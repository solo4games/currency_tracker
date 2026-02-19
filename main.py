"""
Currency Tracker - приложение для периодического сбора курсов валют
"""
import sys
from config import Config
from container import create_container


def main():
    Config.setup_logging()

    container = create_container()

    scheduler = container.resolve('SchedulerController')
    scheduler.start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Планировщик остановлен пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"Критическая ошибка: {e}", file=sys.stderr)
        sys.exit(1)