#!/usr/bin/env python3
"""
Примеры тестирования инструмента визуализации зависимостей.
Этапы 1-2.
"""

import os
import subprocess
import json


def create_test_repository():
    """Создание тестового репозитория для демонстрации."""
    os.makedirs('test_data', exist_ok=True)
    
    # Создаём тестовые данные в формате npm
    npm_packages = {
        "express": {
            "name": "express",
            "version": "4.18.2",
            "description": "Fast, unopinionated, minimalist web framework",
            "dependencies": {
                "accepts": "~1.3.8",
                "array-flatten": "1.1.1",
                "body-parser": "1.20.1",
                "content-disposition": "0.5.4",
                "cookie": "0.5.0",
                "debug": "2.6.9",
                "depd": "2.0.0",
                "encodeurl": "~1.0.2",
                "escape-html": "~1.0.3",
                "etag": "~1.8.1"
            }
        },
        "react": {
            "name": "react",
            "version": "18.2.0",
            "description": "React is a JavaScript library for building user interfaces.",
            "dependencies": {
                "loose-envify": "^1.1.0"
            }
        },
        "lodash": {
            "name": "lodash",
            "version": "4.17.21",
            "description": "Lodash modular utilities.",
            "dependencies": {}
        },
        "axios": {
            "name": "axios",
            "version": "1.6.0",
            "description": "Promise based HTTP client for the browser and node.js",
            "dependencies": {
                "follow-redirects": "^1.15.0",
                "form-data": "^4.0.0",
                "proxy-from-env": "^1.1.0"
            }
        },
        "webpack": {
            "name": "webpack",
            "version": "5.89.0",
            "description": "Packs CommonJs/AMD modules for the browser.",
            "dependencies": {
                "@types/eslint-scope": "^3.7.3",
                "@webassemblyjs/ast": "^1.11.5",
                "acorn": "^8.7.1",
                "browserslist": "^4.14.5",
                "chrome-trace-event": "^1.0.2",
                "enhanced-resolve": "^5.15.0",
                "es-module-lexer": "^1.2.1"
            }
        }
    }
    
    # Сохраняем в JSON файл
    with open('test_data/npm_packages.json', 'w', encoding='utf-8') as f:
        json.dump(npm_packages, f, indent=2, ensure_ascii=False)
    
    print("✓ Тестовый репозиторий npm пакетов создан: test_data/npm_packages.json")
    
    # Создаём альтернативный формат (список пакетов)
    npm_packages_list = {
        "packages": [
            {
                "name": "express",
                "version": "4.18.2",
                "dependencies": ["accepts", "array-flatten", "body-parser", "cookie", "debug"]
            },
            {
                "name": "react",
                "version": "18.2.0",
                "dependencies": ["loose-envify"]
            }
        ]
    }
    
    with open('test_data/npm_packages_list.json', 'w', encoding='utf-8') as f:
        json.dump(npm_packages_list, f, indent=2, ensure_ascii=False)
    
    print("✓ Альтернативный формат создан: test_data/npm_packages_list.json")


def run_test(description, command):
    """
    Запуск тестовой команды.
    
    Args:
        description: Описание теста
        command: Команда для выполнения
    """
    print(f"\n{'=' * 60}")
    print(f"ТЕСТ: {description}")
    print(f"{'=' * 60}")
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
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ ИНСТРУМЕНТА ВИЗУАЛИЗАЦИИ ЗАВИСИМОСТЕЙ")
    print("Этапы 1-2: Конфигурация и сбор данных о зависимостях")
    print("=" * 60)
    print()
    
    # Создание тестового репозитория
    create_test_repository()
    
    # ===== ЭТАП 1: Тесты конфигурации =====
    print(f"\n{'#' * 60}")
    print("# ЭТАП 1: ТЕСТЫ КОНФИГУРАЦИИ")
    print(f"{'#' * 60}")
    
    # Тест 1: Базовая конфигурация
    run_test(
        "Этап 1: Базовая конфигурация с тестовым репозиторием",
        "python dependency_visualizer.py -p express -r test_data/npm_packages.json -t"
    )
    
    # Тест 2: Конфигурация с фильтром
    run_test(
        "Этап 1: Конфигурация с фильтром",
        'python dependency_visualizer.py -p express -r test_data/npm_packages.json -t -f "body"'
    )
    
    # ===== ЭТАП 2: Тесты анализа зависимостей =====
    print(f"\n{'#' * 60}")
    print("# ЭТАП 2: ТЕСТЫ АНАЛИЗА ЗАВИСИМОСТЕЙ")
    print(f"{'#' * 60}")
    
    # Тест 3: Анализ express
    run_test(
        "Этап 2: Анализ зависимостей express",
        "python dependency_visualizer.py -p express -r test_data/npm_packages.json -t"
    )
    
    # Тест 4: Анализ react
    run_test(
        "Этап 2: Анализ зависимостей react",
        "python dependency_visualizer.py -p react -r test_data/npm_packages.json -t"
    )
    
    # Тест 5: Анализ lodash (без зависимостей)
    run_test(
        "Этап 2: Анализ lodash (пакет без зависимостей)",
        "python dependency_visualizer.py -p lodash -r test_data/npm_packages.json -t"
    )
    
    # Тест 6: Анализ с фильтрацией
    run_test(
        "Этап 2: Анализ webpack с фильтром 'resolve'",
        'python dependency_visualizer.py -p webpack -r test_data/npm_packages.json -t -f "resolve"'
    )
    
    # Тест 7: Альтернативный формат данных
    run_test(
        "Этап 2: Работа с альтернативным форматом (список пакетов)",
        "python dependency_visualizer.py -p express -r test_data/npm_packages_list.json -t"
    )
    
    # ===== ТЕСТЫ ОБРАБОТКИ ОШИБОК =====
    print(f"\n{'#' * 60}")
    print("# ТЕСТЫ ОБРАБОТКИ ОШИБОК")
    print(f"{'#' * 60}")
    
    # Тест 8: Несуществующий пакет
    run_test(
        "Ошибка: Несуществующий пакет",
        "python dependency_visualizer.py -p nonexistent-package -r test_data/npm_packages.json -t"
    )
    
    # Тест 9: Несуществующий файл
    run_test(
        "Ошибка: Несуществующий файл репозитория",
        "python dependency_visualizer.py -p express -r nonexistent.json -t"
    )
    
    # Тест 10: Пустое имя пакета
    run_test(
        "Ошибка: Пустое имя пакета",
        'python dependency_visualizer.py -p "" -r test_data/npm_packages.json -t'
    )
    
    # ===== ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ =====
    print(f"\n{'#' * 60}")
    print("# ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ")
    print(f"{'#' * 60}")
    
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
    
    # ===== ИНСТРУКЦИЯ ПО РАБОТЕ С РЕАЛЬНЫМ NPM =====
    print(f"\n{'#' * 60}")
    print("# РАБОТА С РЕАЛЬНЫМ NPM REGISTRY")
    print(f"{'#' * 60}")
    print("""
Для работы с реальными npm пакетами используйте:

python dependency_visualizer.py -p express -r https://registry.npmjs.org

Примеры популярных пакетов для тестирования:
- express (веб-фреймворк)
- react (UI библиотека)
- lodash (утилиты)
- axios (HTTP клиент)
- webpack (сборщик модулей)

ВНИМАНИЕ: Для работы с registry.npmjs.org требуется интернет-соединение!
    """)
    
    print(f"\n{'=' * 60}")
    print("ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ")
    print(f"{'=' * 60}")


if __name__ == '__main__':
    main()
