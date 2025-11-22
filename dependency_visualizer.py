#!/usr/bin/env python3
"""
Инструмент визуализации графа зависимостей для менеджера пакетов.
Этап 1: Минимальный прототип с конфигурацией.
"""

import argparse
import sys
import os
from typing import Optional
from pathlib import Path


class ConfigError(Exception):
    """Исключение для ошибок конфигурации."""
    pass


class DependencyVisualizer:
    """Класс для визуализации графа зависимостей пакетов."""

    def __init__(self, package_name: str, repo_url: str,
                 test_mode: bool = False, filter_substring: Optional[str] = None):
        """
        Инициализация визуализатора зависимостей.

        Args:
            package_name: Имя анализируемого пакета
            repo_url: URL-адрес репозитория или путь к файлу тестового репозитория
            test_mode: Режим работы с тестовым репозиторием
            filter_substring: Подстрока для фильтрации пакетов
        """
        self.package_name = package_name
        self.repo_url = repo_url
        self.test_mode = test_mode
        self.filter_substring = filter_substring

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
                    self.repo_url.startswith('https://') or
                    self.repo_url.startswith('git://')):
                raise ConfigError(
                    f"Некорректный URL репозитория: {self.repo_url}. "
                    "URL должен начинаться с http://, https:// или git://"
                )

        # Проверка подстроки фильтрации
        if self.filter_substring is not None and len(self.filter_substring) > 100:
            raise ConfigError(
                "Подстрока для фильтрации слишком длинная (максимум 100 символов)"
            )

    def print_config(self) -> None:
        """Вывод конфигурации в формате ключ-значение."""
        print("=" * 60)
        print("КОНФИГУРАЦИЯ ИНСТРУМЕНТА ВИЗУАЛИЗАЦИИ ЗАВИСИМОСТЕЙ")
        print("=" * 60)
        print(f"Имя пакета:              {self.package_name}")
        print(f"URL/Путь репозитория:    {self.repo_url}")
        print(f"Тестовый режим:          {'Включен' if self.test_mode else 'Выключен'}")
        print(f"Фильтр пакетов:          {self.filter_substring if self.filter_substring else 'Не установлен'}")
        print("=" * 60)


def parse_arguments() -> argparse.Namespace:
    """
    Парсинг аргументов командной строки.

    Returns:
        Namespace с распарсенными аргументами
    """
    parser = argparse.ArgumentParser(
        description='Инструмент визуализации графа зависимостей для менеджера пакетов',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  %(prog)s -p numpy -r https://pypi.org/simple
  %(prog)s -p requests -r ./test_repo.json -t -f "http"
  %(prog)s --package pandas --repo https://github.com/pypa/simple --filter "data"
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
        help='URL-адрес репозитория или путь к файлу тестового репозитория (обязательный параметр)'
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
        '-v', '--version',
        action='version',
        version='%(prog)s 0.1.0 (Этап 1)'
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
            filter_substring=args.filter
        )

        # Валидация конфигурации
        visualizer.validate_config()

        # Вывод конфигурации
        visualizer.print_config()

        print("\n✓ Конфигурация успешно загружена и проверена!")
        return 0

    except ConfigError as e:
        print(f"\n✗ Ошибка конфигурации: {e}", file=sys.stderr)
        return 1

    except KeyboardInterrupt:
        print("\n\n✗ Выполнение прервано пользователем", file=sys.stderr)
        return 1

    except Exception as e:
        print(f"\n✗ Неожиданная ошибка: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
