import logging

import dotenv

from app import run

dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("apscheduler").setLevel(logging.WARNING)


def main():
    run()


if __name__ == '__main__':
    main()
