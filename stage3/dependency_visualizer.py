#!/usr/bin/env python3
"""
Инструмент визуализации графа зависимостей для менеджера пакетов.
Этапы 1-3: CLI-приложение с построением графа зависимостей.
"""

import argparse
import sys
import json
import urllib.request
import urllib.error
from typing import Optional, Dict, List, Set, Tuple
from pathlib import Path
from collections import deque


class ConfigError(Exception):
    """Исключение для ошибок конфигурации."""
    pass


class DependencyError(Exception):
    """Исключение для ошибок при получении зависимостей."""
    pass


class DependencyGraph:
    """Класс для представления графа зависимостей."""
    
    def __init__(self):
        """Инициализация графа."""
        self.nodes: Set[str] = set()
        self.edges: Dict[str, Set[str]] = {}
        self.cycles: List[List[str]] = []
    
    def add_node(self, node: str) -> None:
        """Добавление узла в граф."""
        self.nodes.add(node)
        if node not in self.edges:
            self.edges[node] = set()
    
    def add_edge(self, from_node: str, to_node: str) -> None:
        """Добавление ребра в граф."""
        self.add_node(from_node)
        self.add_node(to_node)
        self.edges[from_node].add(to_node)
    
    def has_edge(self, from_node: str, to_node: str) -> bool:
        """Проверка наличия ребра."""
        return from_node in self.edges and to_node in self.edges[from_node]
    
    def get_dependencies(self, node: str) -> Set[str]:
        """Получение зависимостей узла."""
        return self.edges.get(node, set())


class DependencyVisualizer:
    """Класс для визуализации графа зависимостей пакетов."""
    
    def __init__(self, package_name: str, repo_url: str, 
                 test_mode: bool = False, filter_substring: Optional[str] = None,
                 max_depth: int = 10):
        """
        Инициализация визуализатора зависимостей.
        
        Args:
            package_name: Имя анализируемого пакета
            repo_url: URL-адрес репозитория или путь к файлу тестового репозитория
            test_mode: Режим работы с тестовым репозиторием
            filter_substring: Подстрока для фильтрации (исключения) пакетов
            max_depth: Максимальная глубина анализа зависимостей
        """
        self.package_name = package_name
        self.repo_url = repo_url
        self.test_mode = test_mode
        self.filter_substring = filter_substring
        self.max_depth = max_depth
        self.dependencies_cache: Dict[str, Dict] = {}
        self.graph = DependencyGraph()
        self.visited: Set[str] = set()
        self.in_progress: Set[str] = set()
        
    def validate_config(self) -> None:
        """
        Валидация конфигурации.
        
        Raises:
            ConfigError: При обнаружении ошибок в конфигурации
        """
        # Проверка имени пакета
        if not self.package_name or not self.package_name.strip():
            raise ConfigError("Имя пакета не может быть пустым")
        
        if len(self.package_name) > 255:
            raise ConfigError("Имя пакета слишком длинное (максимум 255 символов)")
        
        # Проверка URL репозитория или пути
        if not self.repo_url or not self.repo_url.strip():
            raise ConfigError("URL репозитория или путь к файлу не может быть пустым")
        
        # Если включен тестовый режим, проверяем существование файла
        if self.test_mode:
            repo_path = Path(self.repo_url)
            if not repo_path.exists():
                raise ConfigError(
                    f"Тестовый репозиторий не найден по пути: {self.repo_url}"
                )
            if not repo_path.is_file() and not repo_path.is_dir():
                raise ConfigError(
                    f"Путь должен указывать на файл или директорию: {self.repo_url}"
                )
        else:
            # Простая проверка формата URL
            if not (self.repo_url.startswith('http://') or 
                    self.repo_url.startswith('https://')):
                raise ConfigError(
                    f"Некорректный URL репозитория: {self.repo_url}. "
                    "URL должен начинаться с http:// или https://"
                )
        
        # Проверка подстроки фильтрации
        if self.filter_substring is not None and len(self.filter_substring) > 100:
            raise ConfigError(
                "Подстрока для фильтрации слишком длинная (максимум 100 символов)"
            )
    
    def should_skip_package(self, package_name: str) -> bool:
        """
        Проверка, нужно ли пропустить пакет при анализе.
        
        Args:
            package_name: Имя пакета
            
        Returns:
            True, если пакет нужно пропустить
        """
        if self.filter_substring and self.filter_substring.lower() in package_name.lower():
            return True
        return False
    
    def fetch_package_info_npm(self, package_name: str) -> Dict:
        """
        Получение информации о пакете из npm registry.
        
        Args:
            package_name: Имя пакета
            
        Returns:
            Словарь с информацией о пакете
            
        Raises:
            DependencyError: При ошибке получения данных
        """
        if package_name in self.dependencies_cache:
            return self.dependencies_cache[package_name]
        
        try:
            # Формируем URL для npm registry
            url = f"{self.repo_url}/{package_name}"
            
            # Создаём запрос с заголовками
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'DependencyVisualizer/0.3.0',
                    'Accept': 'application/json'
                }
            )
            
            # Выполняем запрос
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                self.dependencies_cache[package_name] = data
                return data
                
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise DependencyError(f"Пакет '{package_name}' не найден в репозитории")
            else:
                raise DependencyError(f"HTTP ошибка {e.code} при получении пакета '{package_name}'")
        except urllib.error.URLError as e:
            raise DependencyError(f"Ошибка соединения: {e.reason}")
        except json.JSONDecodeError:
            raise DependencyError(f"Ошибка парсинга JSON для пакета '{package_name}'")
        except Exception as e:
            raise DependencyError(f"Неожиданная ошибка при получении пакета '{package_name}': {e}")
    
    def fetch_package_info_test(self, package_name: str) -> Dict:
        """
        Получение информации о пакете из тестового репозитория.
        
        Args:
            package_name: Имя пакета
            
        Returns:
            Словарь с информацией о пакете
            
        Raises:
            DependencyError: При ошибке получения данных
        """
        try:
            repo_path = Path(self.repo_url)
            
            # Если это директория, ищем файл пакета
            if repo_path.is_dir():
                package_file = repo_path / f"{package_name}.json"
                if not package_file.exists():
                    raise DependencyError(f"Пакет '{package_name}' не найден в тестовом репозитории")
                with open(package_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            # Если это файл, читаем его как базу данных пакетов
            else:
                with open(repo_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Поддержка разных форматов тестовых данных
                if isinstance(data, dict):
                    if 'packages' in data:
                        # Формат: {"packages": [{"name": "...", ...}, ...]}
                        for pkg in data['packages']:
                            if pkg.get('name') == package_name:
                                return pkg
                    elif package_name in data:
                        # Формат: {"package_name": {...}, ...}
                        return data[package_name]
                
                raise DependencyError(f"Пакет '{package_name}' не найден в тестовом репозитории")
                
        except FileNotFoundError:
            raise DependencyError(f"Файл тестового репозитория не найден: {self.repo_url}")
        except json.JSONDecodeError:
            raise DependencyError(f"Ошибка парсинга JSON в файле: {self.repo_url}")
        except Exception as e:
            raise DependencyError(f"Ошибка чтения тестового репозитория: {e}")
    
    def get_package_dependencies(self, package_name: str) -> Dict[str, str]:
        """
        Получение прямых зависимостей пакета.
        
        Args:
            package_name: Имя пакета
            
        Returns:
            Словарь зависимостей {имя: версия}
        """
        if self.test_mode:
            package_info = self.fetch_package_info_test(package_name)
        else:
            package_info = self.fetch_package_info_npm(package_name)
        
        # Извлечение зависимостей в зависимости от формата
        dependencies = {}
        
        # Формат npm registry
        if 'dist-tags' in package_info and 'versions' in package_info:
            latest_version = package_info['dist-tags'].get('latest')
            if latest_version and latest_version in package_info['versions']:
                version_info = package_info['versions'][latest_version]
                dependencies = version_info.get('dependencies', {})
        
        # Упрощённый формат (для тестов)
        elif 'dependencies' in package_info:
            dependencies = package_info['dependencies']
            # Если зависимости - список строк, преобразуем в словарь
            if isinstance(dependencies, list):
                dependencies = {dep: '*' for dep in dependencies}
        
        return dependencies
    
    def build_dependency_graph_bfs(self, root_package: str, current_depth: int = 0) -> None:
        """
        Построение графа зависимостей с использованием BFS с рекурсией.
        
        Args:
            root_package: Корневой пакет для анализа
            current_depth: Текущая глубина рекурсии
        """
        # Проверка максимальной глубины
        if current_depth > self.max_depth:
            return
        
        # Пропускаем пакеты с фильтруемой подстрокой
        if self.should_skip_package(root_package):
            return
        
        # Обнаружение циклических зависимостей
        if root_package in self.in_progress:
            # Найден цикл
            return
        
        # Если уже обрабатывали этот пакет
        if root_package in self.visited:
            return
        
        # Помечаем как обрабатываемый
        self.in_progress.add(root_package)
        
        try:
            # Получаем зависимости текущего пакета
            dependencies = self.get_package_dependencies(root_package)
            
            # Добавляем узел в граф
            self.graph.add_node(root_package)
            
            # Создаём очередь для BFS (ширина)
            queue = deque()
            
            # Добавляем все зависимости в граф и очередь
            for dep_name, dep_version in dependencies.items():
                # Пропускаем фильтруемые пакеты
                if self.should_skip_package(dep_name):
                    continue
                
                # Добавляем ребро в граф
                self.graph.add_edge(root_package, dep_name)
                
                # Добавляем в очередь для дальнейшей обработки
                if dep_name not in self.visited:
                    queue.append(dep_name)
            
            # Помечаем как посещённый
            self.visited.add(root_package)
            self.in_progress.remove(root_package)
            
            # Рекурсивно обрабатываем все зависимости из очереди (BFS)
            for dep_name in queue:
                try:
                    self.build_dependency_graph_bfs(dep_name, current_depth + 1)
                except DependencyError as e:
                    # Если пакет не найден, пропускаем его
                    print(f"⚠ Предупреждение: {e}", file=sys.stderr)
                    continue
                    
        except DependencyError as e:
            self.in_progress.discard(root_package)
            raise e
    
    def detect_cycles(self) -> List[List[str]]:
        """
        Обнаружение циклических зависимостей в графе.
        
        Returns:
            Список найденных циклов
        """
        cycles = []
        visited = set()
        rec_stack = []
        
        def dfs(node: str, path: List[str]) -> None:
            """DFS для поиска циклов."""
            if node in path:
                # Найден цикл
                cycle_start = path.index(node)
                cycle = path[cycle_start:] + [node]
                cycles.append(cycle)
                return
            
            if node in visited:
                return
            
            visited.add(node)
            path.append(node)
            
            for neighbor in self.graph.get_dependencies(node):
                dfs(neighbor, path.copy())
        
        # Запускаем DFS от каждого узла
        for node in self.graph.nodes:
            dfs(node, [])
        
        return cycles
    
    def print_graph(self) -> None:
        """Вывод графа зависимостей в текстовом формате."""
        print(f"\n{'=' * 60}")
        print(f"ГРАФ ЗАВИСИМОСТЕЙ ПАКЕТА: {self.package_name}")
        print(f"{'=' * 60}\n")
        
        if not self.graph.nodes:
            print("✗ Граф пустой")
            return
        
        print(f"Всего узлов (пакетов): {len(self.graph.nodes)}")
        total_edges = sum(len(deps) for deps in self.graph.edges.values())
        print(f"Всего рёбер (зависимостей): {total_edges}")
        
        if self.filter_substring:
            print(f"Исключены пакеты, содержащие: '{self.filter_substring}'")
        
        print(f"\nСтруктура зависимостей:\n")
        
        # Выводим дерево зависимостей
        self._print_tree(self.package_name, set(), "")
        
        # Проверка на циклические зависимости
        cycles = self.detect_cycles()
        if cycles:
            print(f"\n{'!' * 60}")
            print(f"⚠ ОБНАРУЖЕНЫ ЦИКЛИЧЕСКИЕ ЗАВИСИМОСТИ: {len(cycles)}")
            print(f"{'!' * 60}\n")
            for i, cycle in enumerate(cycles, 1):
                print(f"Цикл {i}: {' → '.join(cycle)}")
        else:
            print(f"\n✓ Циклических зависимостей не обнаружено")
        
        print(f"\n{'=' * 60}")
    
    def _print_tree(self, node: str, visited: Set[str], prefix: str) -> None:
        """
        Рекурсивный вывод дерева зависимостей.
        
        Args:
            node: Текущий узел
            visited: Множество посещённых узлов (для предотвращения бесконечной рекурсии)
            prefix: Префикс для форматирования вывода
        """
        # Предотвращаем бесконечную рекурсию при циклах
        if node in visited:
            print(f"{prefix}└─ {node} (циклическая зависимость)")
            return
        
        print(f"{prefix}{node}")
        visited.add(node)
        
        dependencies = sorted(self.graph.get_dependencies(node))
        
        for i, dep in enumerate(dependencies):
            is_last = (i == len(dependencies) - 1)
            connector = "└─ " if is_last else "├─ "
            extension = "   " if is_last else "│  "
            
            if dep in visited:
                print(f"{prefix}{connector}{dep} (циклическая зависимость)")
            else:
                print(f"{prefix}{connector}{dep}")
                self._print_tree(dep, visited.copy(), prefix + extension)
    
    def analyze_dependencies(self) -> None:
        """Анализ и построение полного графа зависимостей."""
        try:
            print(f"Анализ зависимостей для пакета '{self.package_name}'...")
            print(f"Максимальная глубина: {self.max_depth}")
            
            if self.filter_substring:
                print(f"Исключаются пакеты, содержащие: '{self.filter_substring}'")
            
            # Построение графа
            self.build_dependency_graph_bfs(self.package_name)
            
            # Вывод графа
            self.print_graph()
            
        except DependencyError as e:
            print(f"✗ Ошибка при анализе зависимостей: {e}", file=sys.stderr)
            sys.exit(1)


def parse_arguments() -> argparse.Namespace:
    """
    Парсинг аргументов командной строки.
    
    Returns:
        Namespace с распарсенными аргументами
    """
    parser = argparse.ArgumentParser(
        description='Инструмент визуализации графа зависимостей для менеджера пакетов npm',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  # Анализ npm пакета
  %(prog)s -p express -r https://registry.npmjs.org
  
  # Работа с тестовым репозиторием
  %(prog)s -p A -r ./test_data/graph_test.json -t
  
  # Исключение пакетов с подстрокой "dev"
  %(prog)s -p react -r https://registry.npmjs.org -f "dev"
  
  # Ограничение глубины анализа
  %(prog)s -p webpack -r https://registry.npmjs.org -d 3
        """
    )
    
    parser.add_argument(
        '-p', '--package',
        type=str,
        required=True,
        metavar='NAME',
        help='Имя анализируемого пакета (обязательный параметр)'
    )
    
    parser.add_argument(
        '-r', '--repo',
        type=str,
        required=True,
        metavar='URL/PATH',
        help='URL npm registry или путь к файлу тестового репозитория (обязательный параметр)'
    )
    
    parser.add_argument(
        '-t', '--test-mode',
        action='store_true',
        help='Режим работы с тестовым репозиторием'
    )
    
    parser.add_argument(
        '-f', '--filter',
        type=str,
        metavar='SUBSTRING',
        default=None,
        help='Подстрока для исключения пакетов из анализа'
    )
    
    parser.add_argument(
        '-d', '--max-depth',
        type=int,
        metavar='N',
        default=10,
        help='Максимальная глубина анализа зависимостей (по умолчанию: 10)'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 0.3.0 (Этапы 1-3)'
    )
    
    return parser.parse_args()


def main() -> int:
    """
    Главная функция приложения.
    
    Returns:
        Код возврата (0 - успех, 1 - ошибка)
    """
    try:
        # Парсинг аргументов командной строки
        args = parse_arguments()
        
        # Создание экземпляра визуализатора
        visualizer = DependencyVisualizer(
            package_name=args.package,
            repo_url=args.repo,
            test_mode=args.test_mode,
            filter_substring=args.filter,
            max_depth=args.max_depth
        )
        
        # Валидация конфигурации
        visualizer.validate_config()
        
        # Анализ зависимостей и построение графа
        visualizer.analyze_dependencies()
        
        print("\n✓ Анализ успешно завершён!")
        return 0
        
    except ConfigError as e:
        print(f"\n✗ Ошибка конфигурации: {e}", file=sys.stderr)
        return 1
    
    except DependencyError as e:
        print(f"\n✗ Ошибка получения зависимостей: {e}", file=sys.stderr)
        return 1
    
    except KeyboardInterrupt:
        print("\n\n✗ Выполнение прервано пользователем", file=sys.stderr)
        return 1
    
    except Exception as e:
        print(f"\n✗ Неожиданная ошибка: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
