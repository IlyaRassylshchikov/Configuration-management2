#!/usr/bin/env python3
"""
Примеры тестирования инструмента визуализации зависимостей.
Этапы 1-5.
"""

import os
import subprocess
import json


def create_test_repositories():
    """Создание тестовых репозиториев для демонстрации."""
    os.makedirs('test_data', exist_ok=True)
    os.makedirs('visualizations', exist_ok=True)
    
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
    print("Этапы 1-5: Визуализация на языке Mermaid")
    print("=" * 70)
    print()
    
    # Создание тестовых репозиториев
    create_test_repositories()
    
    # ===== ЭТАП 5: ВИЗУАЛИЗАЦИЯ В ФОРМАТЕ MERMAID =====
    print(f"\n{'#' * 70}")
    print("# ЭТАП 5: ВИЗУАЛИЗАЦИЯ В ФОРМАТЕ MERMAID")
    print(f"{'#' * 70}")
    
    # Тест 1: Простой граф - вывод на экран
    run_test(
        "Визуализация простого графа в формате Mermaid",
        "python dependency_visualizer.py -p A -r test_data/simple_graph.json -t --mermaid"
    )
    
    # Тест 2: Простой граф - сохранение в файл
    run_test(
        "Сохранение визуализации в файл",
        "python dependency_visualizer.py -p A -r test_data/simple_graph.json -t -m -o visualizations/simple_graph.md"
    )
    
    # Тест 3: Граф с циклами
    run_test(
        "Визуализация графа с циклическими зависимостями",
        "python dependency_visualizer.py -p A -r test_data/cyclic_graph.json -t -m -o visualizations/cyclic_graph.md"
    )
    
    # Тест 4: Сложный граф
    run_test(
        "Визуализация сложного графа с множественными циклами",
        "python dependency_visualizer.py -p A -r test_data/complex_graph.json -t -m -o visualizations/complex_graph.md"
    )
    
    # Тест 5: Широкий граф
    run_test(
        "Визуализация широкого графа",
        "python dependency_visualizer.py -p A -r test_data/wide_graph.json -t -m -o visualizations/wide_graph.md"
    )
    
    # Тест 6: Глубокий граф
    run_test(
        "Визуализация глубокого графа",
        "python dependency_visualizer.py -p A -r test_data/deep_graph.json -t -m -o visualizations/deep_graph.md"
    )
    
    # Тест 7: Граф с фильтрацией
    run_test(
        "Визуализация с фильтрацией (_DEV пакеты)",
        "python dependency_visualizer.py -p A -r test_data/filtered_graph.json -t -f _DEV -m -o visualizations/filtered_graph.md"
    )
    
    # ===== СРАВНЕНИЕ ФОРМАТОВ ВЫВОДА =====
    print(f"\n{'#' * 70}")
    print("# СРАВНЕНИЕ: ТЕКСТОВЫЙ vs MERMAID")
    print(f"{'#' * 70}")
    
    run_test(
        "Текстовый формат (по умолчанию)",
        "python dependency_visualizer.py -p A -r test_data/simple_graph.json -t"
    )
    
    run_test(
        "Формат Mermaid",
        "python dependency_visualizer.py -p A -r test_data/simple_graph.json -t --mermaid"
    )
    
    # ===== ДЕМОНСТРАЦИЯ ТРЕХ РАЗЛИЧНЫХ ПАКЕТОВ =====
    print(f"\n{'#' * 70}")
    print("# ДЕМОНСТРАЦИЯ: ТРИ РАЗЛИЧНЫХ ПАКЕТА")
    print(f"{'#' * 70}")
    
    # Пакет 1: Простой граф
    run_test(
        "Пакет 1: Простая структура зависимостей",
        "python dependency_visualizer.py -p A -r test_data/simple_graph.json -t -m -o visualizations/package1.md"
    )
    
    # Пакет 2: Граф с циклами
    run_test(
        "Пакет 2: Граф с циклическими зависимостями",
        "python dependency_visualizer.py -p A -r test_data/cyclic_graph.json -t -m -o visualizations/package2.md"
    )
    
    # Пакет 3: Широкий граф
    run_test(
        "Пакет 3: Множество прямых зависимостей",
        "python dependency_visualizer.py -p A -r test_data/wide_graph.json -t -m -o visualizations/package3.md"
    )
    
    # ===== ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ =====
    print(f"\n{'#' * 70}")
    print("# ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ")
    print(f"{'#' * 70}")
    
    # Тест справки
    run_test(
        "Вывод справки с новыми параметрами",
        "python dependency_visualizer.py --help"
    )
    
    # Тест версии
    run_test(
        "Вывод версии",
        "python dependency_visualizer.py --version"
    )
    
    # ===== ИНФОРМАЦИЯ О СОЗДАННЫХ ФАЙЛАХ =====
    print(f"\n{'#' * 70}")
    print("# СОЗДАННЫЕ ВИЗУАЛИЗАЦИИ")
    print(f"{'#' * 70}")
    print("""
Создано файлов визуализации в директории 'visualizations/':

1. simple_graph.md      - Простой граф без циклов
2. cyclic_graph.md      - Граф с циклическими зависимостями
3. complex_graph.md     - Сложный граф с множественными циклами
4. wide_graph.md        - Широкий граф
5. deep_graph.md        - Глубокий граф
6. filtered_graph.md    - Граф с фильтрацией
7. package1.md          - Демонстрация пакета 1
8. package2.md          - Демонстрация пакета 2
9. package3.md          - Демонстрация пакета 3

Для просмотра диаграмм:
1. Откройте любой .md файл в текстовом редакторе
2. Скопируйте код между ```mermaid и ```
3. Вставьте на https://mermaid.live
4. Или используйте GitHub для просмотра (GitHub поддерживает Mermaid)
    """)
    
    # ===== ОБЪЯСНЕНИЕ РАЗЛИЧИЙ =====
    print(f"\n{'#' * 70}")
    print("# СРАВНЕНИЕ С ШТАТНЫМИ ИНСТРУМЕНТАМИ ВИЗУАЛИЗАЦИИ")
    print(f"{'#' * 70}")
    print("""
СРАВНЕНИЕ С npm:

1. npm ls --all
   - Показывает дерево установленных зависимостей
   - Учитывает разные версии одного пакета
   - Отображает физическую структуру node_modules
   
   Наш инструмент:
   - Показывает логический граф зависимостей
   - Работает с одной версией каждого пакета
   - Не требует установки пакетов

2. npm explain <package>
   - Показывает, почему пакет установлен
   - Отображает все пути к пакету
   
   Наш инструмент:
   - Показывает полный граф всех зависимостей
   - Визуализирует структуру графа

3. Визуализация npm (npm-graph, dependency-cruiser):
   - Создают изображения в форматах PNG, SVG
   - Используют graphviz/dot для рендеринга
   - Требуют установки дополнительных инструментов
   
   Наш инструмент:
   - Генерирует Mermaid код (текстовый формат)
   - Не требует дополнительных инструментов
   - Легко интегрируется с Markdown и GitHub

РАЗЛИЧИЯ В РЕЗУЛЬТАТАХ:

1. Версии пакетов:
   npm: Может показывать несколько версий одного пакета
   Наш: Работает с единственной (latest) версией

2. Dev dependencies:
   npm: Разделяет dependencies и devDependencies
   Наш: Можно исключить через фильтр (-f "dev")

3. Peer dependencies:
   npm: Специальная обработка peer dependencies
   Наш: Не различает типы зависимостей

4. Оптимизация:
   npm: Показывает оптимизированную структуру (hoisting)
   Наш: Показывает логическую структуру без оптимизаций

5. Циклы:
   npm: Разрывает циклы через peer dependencies
   Наш: Обнаруживает и помечает циклы визуально

ПРЕИМУЩЕСТВА НАШЕГО ПОДХОДА:
-  Простой текстовый формат (Mermaid)
-  Интеграция с GitHub и Markdown
-  Не требует установки пакетов
-  Наглядная визуализация циклов
-  Легко редактировать и модифицировать

ПРЕИМУЩЕСТВА npm инструментов:
-  Учёт реальной установки
-  Поддержка множественных версий
-  Оптимизация структуры
-  Разрешение конфликтов
    """)
    
    print(f"\n{'=' * 70}")
    print("ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ")
    print(f"{'=' * 70}")
    print("\nДля работы с реальными npm пакетами используйте:")
    print("python dependency_visualizer.py -p <package_name> -r https://registry.npmjs.org --mermaid")


if __name__ == '__main__':
    main()
