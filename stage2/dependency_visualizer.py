#!/usr/bin/env python3
"""
Инструмент визуализации графа зависимостей для менеджера пакетов.
Этапы 1-2: CLI-приложение с извлечением зависимостей npm пакетов.
"""

import argparse
import sys
import json
import urllib.request
import urllib.error
from typing import Optional, Dict, List, Set
from pathlib import Path


class ConfigError(Exception):
    """Исключение для ошибок конфигурации."""
    pass


class DependencyError(Exception):
    """Исключение для ошибок при получении зависимостей."""
    pass


class DependencyVisualizer:
    """Класс для визуализации графа зависимостей пакетов."""
    
    def __init__(self, package_name: str, repo_url: str, 
                 test_mode: bool = False, filter_substring: Optional[str] = None,
                 max_depth: int = 1):
        """
        Инициализация визуализатора зависимостей.
        
        Args:
            package_name: Имя анализируемого пакета
            repo_url: URL-адрес репозитория или путь к файлу тестового репозитория
            test_mode: Режим работы с тестовым репозиторием
            filter_substring: Подстрока для фильтрации пакетов
            max_depth: Максимальная глубина анализа зависимостей
        """
        self.package_name = package_name
        self.repo_url = repo_url
        self.test_mode = test_mode
        self.filter_substring = filter_substring
        self.max_depth = max_depth
        self.dependencies_cache: Dict[str, Dict] = {}
        
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
                    'User-Agent': 'DependencyVisualizer/0.2.0',
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
        
        # Применение фильтра
        if self.filter_substring:
            dependencies = {
                name: version for name, version in dependencies.items()
                if self.filter_substring.lower() in name.lower()
            }
        
        return dependencies
    
    def print_dependencies(self, package_name: str, indent: int = 0) -> None:
        """
        Вывод зависимостей пакета на экран.
        
        Args:
            package_name: Имя пакета
            indent: Уровень отступа для вложенности
        """
        prefix = "  " * indent
        
        try:
            dependencies = self.get_package_dependencies(package_name)
            
            if not dependencies:
                print(f"{prefix}└─ (нет зависимостей)")
                return
            
            dep_count = len(dependencies)
            for i, (dep_name, dep_version) in enumerate(dependencies.items(), 1):
                is_last = (i == dep_count)
                connector = "└─" if is_last else "├─"
                print(f"{prefix}{connector} {dep_name} ({dep_version})")
                
        except DependencyError as e:
            print(f"{prefix}└─ ✗ Ошибка: {e}")
    
    def analyze_dependencies(self) -> None:
        """Анализ и вывод всех прямых зависимостей пакета."""
        print(f"{'=' * 60}")
        print(f"АНАЛИЗ ЗАВИСИМОСТЕЙ ПАКЕТА: {self.package_name}")
        print(f"{'=' * 60}\n")
        
        try:
            dependencies = self.get_package_dependencies(self.package_name)
            
            if not dependencies:
                print(f"✓ Пакет '{self.package_name}' не имеет зависимостей")
                return
            
            print(f"✓ Найдено прямых зависимостей: {len(dependencies)}\n")
            print(f"{self.package_name}")
            
            dep_count = len(dependencies)
            for i, (dep_name, dep_version) in enumerate(dependencies.items(), 1):
                is_last = (i == dep_count)
                connector = "└─" if is_last else "├─"
                print(f"{connector} {dep_name} @ {dep_version}")
            
            print(f"\n{'=' * 60}")
            
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
  %(prog)s -p mypackage -r ./test_data/npm_repo.json -t
  
  # С фильтрацией зависимостей
  %(prog)s -p react -r https://registry.npmjs.org -f "babel"
        """
    )
    
    parser.add_argument(
        '-p', '--package',
        type=str,
        required=True,
        metavar='NAME',
        help='Имя анализируемого npm пакета (обязательный параметр)'
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
        help='Режим работы с тестовым репозиторием (использовать локальный файл/директорию)'
    )
    
    parser.add_argument(
        '-f', '--filter',
        type=str,
        metavar='SUBSTRING',
        default=None,
        help='Подстрока для фильтрации пакетов (необязательный параметр)'
    )
    
    parser.add_argument(
        '-d', '--max-depth',
        type=int,
        metavar='N',
        default=1,
        help='Максимальная глубина анализа зависимостей (по умолчанию: 1)'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 0.2.0 (Этапы 1-2)'
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
        
        # Анализ зависимостей (Этап 2)
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
        return 1


if __name__ == '__main__':
    sys.exit(main())
