#!/usr/bin/env python3
"""
Примеры тестирования инструмента визуализации зависимостей.
Этапы 1-4.
"""

import os
import subprocess
import json


def create_test_repositories():
    """Создание тестовых репозиториев для демонстрации."""
    os.makedirs('test_data', exist_ok=True)
    
    # Тест 1: Простой граф без циклов
    simple_graph = {
        "A": {
            "name": "A",
            "version": "1.0.0",
            "dependencies": ["B", "C"]
        },
        "B": {
            "name": "B",
            "version": "1.0.0",
            "dependencies": ["D"]
        },
        "C": {
            "name": "C",
            "version": "1.0.0",
            "dependencies": ["D", "E"]
        },
        "D": {
            "name": "D",
            "version": "1.0.0",
            "dependencies": []
        },
        "E": {
            "name": "E",
            "version": "1.0.0",
            "dependencies": []
        }
    }
    
    with open('test_data/simple_graph.json', 'w', encoding='utf-8') as f:
        json.dump(simple_graph, f, indent=2)
    print("✓ Создан тестовый граф: simple_graph.json (простой граф без циклов)")
    
    # Тест 2: Граф с циклическими зависимостями
    cyclic_graph = {
        "A": {
            "name": "A",
            "version": "1.0.0",
            "dependencies": ["B"]
        },
        "B": {
            "name": "B",
            "version": "1.0.0",
            "dependencies": ["C"]
        },
        "C": {
            "name": "C",
            "version": "1.0.0",
            "dependencies": ["A", "D"]
        },
        "D": {
            "name": "D",
            "version": "1.0.0",
            "dependencies": []
        }
    }
    
    with open('test_data/cyclic_graph.json', 'w', encoding='utf-8') as f:
        json.dump(cyclic_graph, f, indent=2)
    print("✓ Создан тестовый граф: cyclic_graph.json (с циклическими зависимостями)")
    
    # Тест 3: Сложный граф с множественными циклами
    complex_graph = {
        "A": {
            "name": "A",
            "version": "1.0.0",
            "dependencies": ["B", "C"]
        },
        "B": {
            "name": "B",
            "version": "1.0.0",
            "dependencies": ["D", "E"]
        },
        "C": {
            "name": "C",
            "version": "1.0.0",
            "dependencies": ["F"]
        },
        "D": {
            "name": "D",
            "version": "1.0.0",
            "dependencies": ["B"]
        },
        "E": {
            "name": "E",
            "version": "1.0.0",
            "dependencies": ["F", "G"]
        },
        "F": {
            "name": "F",
            "version": "1.0.0",
            "dependencies": ["G"]
        },
        "G": {
            "name": "G",
            "version": "1.0.0",
            "dependencies": ["E"]
        }
    }
    
    with open('test_data/complex_graph.json', 'w', encoding='utf-8') as f:
        json.dump(complex_graph, f, indent=2)
    print("✓ Создан тестовый граф: complex_graph.json (сложный граф с множественными циклами)")
    
    # Тест 4: Граф с пакетами для фильтрации
    filtered_graph = {
        "A": {
            "name": "A",
            "version": "1.0.0",
            "dependencies": ["B", "C_DEV", "D"]
        },
        "B": {
            "name": "B",
            "version": "1.0.0",
            "dependencies": ["E_DEV"]
        },
        "C_DEV": {
            "name": "C_DEV",
            "version": "1.0.0",
            "dependencies": ["F"]
        },
        "D": {
            "name": "D",
            "version": "1.0.0",
            "dependencies": ["G"]
        },
        "E_DEV": {
            "name": "E_DEV",
            "version": "1.0.0",
            "dependencies": []
        },
        "F": {
            "name": "F",
            "version": "1.0.0",
            "dependencies": []
        },
        "G": {
            "name": "G",
            "version": "1.0.0",
            "dependencies": []
        }
    }
    
    with open('test_data/filtered_graph.json', 'w', encoding='utf-8') as f:
        json.dump(filtered_graph, f, indent=2)
    print("✓ Создан тестовый граф: filtered_graph.json (для демонстрации фильтрации)")
    
    # Тест 5: Глубокий граф
    deep_graph = {
        "A": {
            "name": "A",
            "version": "1.0.0",
            "dependencies": ["B"]
        },
        "B": {
            "name": "B",
            "version": "1.0.0",
            "dependencies": ["C"]
        },
        "C": {
            "name": "C",
            "version": "1.0.0",
            "dependencies": ["D"]
        },
        "D": {
            "name": "D",
            "version": "1.0.0",
            "dependencies": ["E"]
        },
        "E": {
            "name": "E",
            "version": "1.0.0",
            "dependencies": ["F"]
        },
        "F": {
            "name": "F",
            "version": "1.0.0",
            "dependencies": ["G"]
        },
        "G": {
            "name": "G",
            "version": "1.0.0",
            "dependencies": ["H"]
        },
        "H": {
            "name": "H",
            "version": "1.0.0",
            "dependencies": []
        }
    }
    
    with open('test_data/deep_graph.json', 'w', encoding='utf-8') as f:
        json.dump(deep_graph, f, indent=2)
    print("✓ Создан тестовый граф: deep_graph.json (глубокий граф для тестирования max-depth)")
    
    # Тест 6: Широкий граф
    wide_graph = {
        "A": {
            "name": "A",
            "version": "1.0.0",
            "dependencies": ["B", "C", "D", "E", "F"]
        },
        "B": {
            "name": "B",
            "version": "1.0.0",
            "dependencies": []
        },
        "C": {
            "name": "C",
            "version": "1.0.0",
            "dependencies": []
        },
        "D": {
            "name": "D",
            "version": "1.0.0",
            "dependencies": []
        },
        "E": {
            "name": "E",
            "version": "1.0.0",
            "dependencies": []
        },
        "F": {
            "name": "F",
            "version": "1.0.0",
            "dependencies": []
        }
    }
    
    with open('test_data/wide_graph.json', 'w', encoding='utf-8') as f:
        json.dump(wide_graph, f, indent=2)
    print("✓ Создан тестовый граф: wide_graph.json (широкий граф)")


def run_test(description, command):
    """
    Запуск тестовой команды.
    
    Args:
        description: Описание теста
        command: Команда для выполнения
    """
    print(f"\n{'=' * 70}")
    print(f"ТЕСТ: {description}")
    print(f"{'=' * 70}")
    print(f"Команда: {command}\n")
    
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    print(f"\nКод возврата: {result.returncode}")


def main():
    """Запуск всех тестов."""
    print("=" * 70)
    print("ДЕМОНСТРАЦИЯ ИНСТРУМЕНТА ВИЗУАЛИЗАЦИИ ЗАВИСИМОСТЕЙ")
    print("Этапы 1-4: Порядок загрузки зависимостей")
    print("=" * 70)
    print()
    
    # Создание тестовых репозиториев
    create_test_repositories()
    
    # ===== ЭТАП 4: ПОРЯДОК ЗАГРУЗКИ ЗАВИСИМОСТЕЙ =====
    print(f"\n{'#' * 70}")
    print("# ЭТАП 4: ПОРЯДОК ЗАГРУЗКИ ЗАВИСИМОСТЕЙ")
    print(f"{'#' * 70}")
    
    # Тест 1: Простой граф - порядок загрузки
    run_test(
        "Порядок загрузки для простого графа без циклов",
        "python dependency_visualizer.py -p A -r test_data/simple_graph.json -t --load-order"
    )
    
    # Тест 2: Граф с циклами - порядок загрузки
    run_test(
        "Порядок загрузки для графа с циклическими зависимостями",
        "python dependency_visualizer.py -p A -r test_data/cyclic_graph.json -t --load-order"
    )
    
    # Тест 3: Сложный граф - порядок загрузки
    run_test(
        "Порядок загрузки для сложного графа с множественными циклами",
        "python dependency_visualizer.py -p A -r test_data/complex_graph.json -t --load-order"
    )
    
    # Тест 4: Глубокий граф - порядок загрузки
    run_test(
        "Порядок загрузки для глубокого графа",
        "python dependency_visualizer.py -p A -r test_data/deep_graph.json -t --load-order"
    )
    
    # Тест 5: Широкий граф - порядок загрузки
    run_test(
        "Порядок загрузки для широкого графа",
        "python dependency_visualizer.py -p A -r test_data/wide_graph.json -t --load-order"
    )
    
    # Тест 6: Порядок загрузки с фильтрацией
    run_test(
        "Порядок загрузки с исключением пакетов '_DEV'",
        "python dependency_visualizer.py -p A -r test_data/filtered_graph.json -t --load-order -f _DEV"
    )
    
    # ===== СРАВНЕНИЕ С ГРАФОМ (без --load-order) =====
    print(f"\n{'#' * 70}")
    print("# СРАВНЕНИЕ: ГРАФ vs ПОРЯДОК ЗАГРУЗКИ")
    print(f"{'#' * 70}")
    
    run_test(
        "Граф зависимостей (обычный режим)",
        "python dependency_visualizer.py -p A -r test_data/simple_graph.json -t"
    )
    
    run_test(
        "Порядок загрузки (режим --load-order)",
        "python dependency_visualizer.py -p A -r test_data/simple_graph.json -t --load-order"
    )
    
    # ===== ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ =====
    print(f"\n{'#' * 70}")
    print("# ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ")
    print(f"{'#' * 70}")
    
    # Тест 7: Справка
    run_test(
        "Вывод справки с новым параметром --load-order",
        "python dependency_visualizer.py --help"
    )
    
    # Тест 8: Версия
    run_test(
        "Вывод версии",
        "python dependency_visualizer.py --version"
    )
    
    # ===== ОБЪЯСНЕНИЕ РАЗЛИЧИЙ =====
    print(f"\n{'#' * 70}")
    print("# ОБЪЯСНЕНИЕ РАБОТЫ ПОРЯДКА ЗАГРУЗКИ")
    print(f"{'#' * 70}")
    print("""
Порядок загрузки зависимостей определяется топологической сортировкой графа.

АЛГОРИТМ (алгоритм Кана):
1. Находим все пакеты без зависимостей (независимые)
2. Добавляем их в порядок загрузки первыми
3. "Удаляем" эти пакеты из графа
4. Повторяем шаги 1-3 для оставшихся пакетов

ПРИМЕР (simple_graph.json):
Граф:  A → B → D
       A → C → D, E

Порядок загрузки:
1. D, E  (нет зависимостей)
2. B, C  (зависят только от D, E)
3. A     (зависит от B, C)

СРАВНЕНИЕ С NPM:
npm использует аналогичную стратегию, но с дополнительными оптимизациями:
- Параллельная загрузка независимых пакетов
- Кеширование уже загруженных версий
- Разрешение конфликтов версий

РАЗЛИЧИЯ:
1. Наш инструмент показывает строгую последовательность
2. npm может загружать независимые пакеты параллельно
3. При наличии циклов npm использует более сложные эвристики

ЦИКЛИЧЕСКИЕ ЗАВИСИМОСТИ:
- Топологическая сортировка невозможна при наличии циклов
- Наш инструмент добавляет оставшиеся пакеты эвристически
- npm обычно разрывает циклы через peer dependencies
    """)
    
    print(f"\n{'=' * 70}")
    print("ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ")
    print(f"{'=' * 70}")
    print("\nДля работы с реальными npm пакетами используйте:")
    print("python dependency_visualizer.py -p <package_name> -r https://registry.npmjs.org --load-order")


if __name__ == '__main__':
    main()
