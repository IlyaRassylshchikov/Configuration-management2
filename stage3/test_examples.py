#!/usr/bin/env python3
"""
Примеры тестирования инструмента визуализации зависимостей.
Этапы 1-3.
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
    print("Этапы 1-3: Построение графа зависимостей с BFS")
    print("=" * 70)
    print()
    
    # Создание тестовых репозиториев
    create_test_repositories()
    
    # ===== ЭТАП 3: ПОСТРОЕНИЕ ГРАФА ЗАВИСИМОСТЕЙ =====
    print(f"\n{'#' * 70}")
    print("# ЭТАП 3: ПОСТРОЕНИЕ ГРАФА ЗАВИСИМОСТЕЙ")
    print(f"{'#' * 70}")
    
    # Тест 1: Простой граф без циклов
    run_test(
        "Простой граф без циклических зависимостей",
        "python dependency_visualizer.py -p A -r test_data/simple_graph.json -t"
    )
    
    # Тест 2: Граф с циклическими зависимостями
    run_test(
        "Граф с циклическими зависимостями (A → B → C → A)",
        "python dependency_visualizer.py -p A -r test_data/cyclic_graph.json -t"
    )
    
    # Тест 3: Сложный граф с множественными циклами
    run_test(
        "Сложный граф с множественными циклами",
        "python dependency_visualizer.py -p A -r test_data/complex_graph.json -t"
    )
    
    # Тест 4: Фильтрация пакетов (исключение DEV пакетов)
    run_test(
        "Фильтрация пакетов: исключение пакетов с '_DEV'",
        "python dependency_visualizer.py -p A -r test_data/filtered_graph.json -t -f _DEV"
    )
    
    # Тест 5: Ограничение глубины анализа
    run_test(
        "Ограничение глубины анализа (max-depth=3)",
        "python dependency_visualizer.py -p A -r test_data/deep_graph.json -t -d 3"
    )
    
    # Тест 6: Широкий граф
    run_test(
        "Широкий граф (много зависимостей на одном уровне)",
        "python dependency_visualizer.py -p A -r test_data/wide_graph.json -t"
    )
    
    # Тест 7: Глубокий граф с полной глубиной
    run_test(
        "Глубокий граф с полным анализом",
        "python dependency_visualizer.py -p A -r test_data/deep_graph.json -t -d 10"
    )
    
    # Тест 8: Анализ отдельного узла без зависимостей
    run_test(
        "Анализ пакета без зависимостей",
        "python dependency_visualizer.py -p D -r test_data/simple_graph.json -t"
    )
    
    # ===== ТЕСТЫ ОБРАБОТКИ ОШИБОК =====
    print(f"\n{'#' * 70}")
    print("# ТЕСТЫ ОБРАБОТКИ ОШИБОК")
    print(f"{'#' * 70}")
    
    # Тест 9: Несуществующий пакет
    run_test(
        "Ошибка: Несуществующий пакет",
        "python dependency_visualizer.py -p Z -r test_data/simple_graph.json -t"
    )
    
    # Тест 10: Несуществующий файл
    run_test(
        "Ошибка: Несуществующий файл репозитория",
        "python dependency_visualizer.py -p A -r test_data/nonexistent.json -t"
    )
    
    # ===== ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ =====
    print(f"\n{'#' * 70}")
    print("# ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ")
    print(f"{'#' * 70}")
    
    # Тест 11: Справка
    run_test(
        "Вывод справки",
        "python dependency_visualizer.py --help"
    )
    
    # Тест 12: Версия
    run_test(
        "Вывод версии",
        "python dependency_visualizer.py --version"
    )
    
    # ===== СВОДНАЯ ИНФОРМАЦИЯ =====
    print(f"\n{'#' * 70}")
    print("# СВОДНАЯ ИНФОРМАЦИЯ О ТЕСТОВЫХ ГРАФАХ")
    print(f"{'#' * 70}")
    print("""
1. simple_graph.json - Простой граф без циклов
   A → B → D
   A → C → D, E
   
2. cyclic_graph.json - Граф с простым циклом
   A → B → C → A (цикл)
   C → D
   
3. complex_graph.json - Сложный граф с множественными циклами
   A → B → D → B (цикл)
   B → E → F → G → E (цикл)
   
4. filtered_graph.json - Граф для демонстрации фильтрации
   Содержит пакеты C_DEV и E_DEV для исключения
   
5. deep_graph.json - Глубокий граф (8 уровней)
   A → B → C → D → E → F → G → H
   
6. wide_graph.json - Широкий граф
   A → [B, C, D, E, F]
    """)
    
    print(f"\n{'=' * 70}")
    print("ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ")
    print(f"{'=' * 70}")
    print("\nДля работы с реальными npm пакетами используйте:")
    print("python dependency_visualizer.py -p <package_name> -r https://registry.npmjs.org")


if __name__ == '__main__':
    main()
