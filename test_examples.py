#!/usr/bin/env python3
"""
Примеры тестирования инструмента визуализации зависимостей.
"""

import os
import subprocess
import json


def create_test_repository():
    """Создание тестового репозитория для демонстрации."""
    os.makedirs('test_data', exist_ok=True)
    
    test_repo = {
        "packages": [
            {
                "name": "requests",
                "version": "2.31.0",
                "dependencies": ["urllib3", "certifi", "charset-normalizer"]
            },
            {
                "name": "flask",
                "version": "3.0.0",
                "dependencies": ["werkzeug", "jinja2", "click"]
            }
        ]
    }
    
    with open('test_data/test_repo.json', 'w', encoding='utf-8') as f:
        json.dump(test_repo, f, indent=2, ensure_ascii=False)
    
    print("✓ Тестовый репозиторий создан: test_data/test_repo.json")


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
    print("ДЕМОНСТРАЦИЯ РАБОТЫ ИНСТРУМЕНТА ВИЗУАЛИЗАЦИИ ЗАВИСИМОСТЕЙ")
    print("Этап 1: Минимальный прототип с конфигурацией\n")
    
    # Создание тестового репозитория
    create_test_repository()
    
    # Тест 1: Успешное выполнение с URL
    run_test(
        "Успешное выполнение с URL репозитория",
        "python dependency_visualizer.py -p numpy -r https://pypi.org/simple"
    )
    
    # Тест 2: Успешное выполнение с тестовым репозиторием
    run_test(
        "Успешное выполнение с тестовым репозиторием",
        "python dependency_visualizer.py -p requests -r test_data/test_repo.json -t"
    )
    
    # Тест 3: Использование фильтра
    run_test(
        "Использование фильтра пакетов",
        'python dependency_visualizer.py -p flask -r https://pypi.org/simple -f "web"'
    )
    
    # Тест 4: Все параметры
    run_test(
        "Все параметры вместе",
        'python dependency_visualizer.py -p requests -r test_data/test_repo.json -t -f "http"'
    )
    
    # Тест 5: Ошибка - пустое имя пакета
    run_test(
        "Ошибка: пустое имя пакета",
        'python dependency_visualizer.py -p "" -r https://pypi.org/simple'
    )
    
    # Тест 6: Ошибка - некорректный URL
    run_test(
        "Ошибка: некорректный URL репозитория",
        "python dependency_visualizer.py -p numpy -r invalid_url"
    )
    
    # Тест 7: Ошибка - несуществующий файл в тестовом режиме
    run_test(
        "Ошибка: несуществующий файл в тестовом режиме",
        "python dependency_visualizer.py -p requests -r nonexistent.json -t"
    )
    
    # Тест 8: Справка
    run_test(
        "Вывод справки",
        "python dependency_visualizer.py --help"
    )
    
    # Тест 9: Версия
    run_test(
        "Вывод версии",
        "python dependency_visualizer.py --version"
    )
    
    print(f"\n{'=' * 60}")
    print("ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ")
    print(f"{'=' * 60}")


if __name__ == '__main__':
    main()
