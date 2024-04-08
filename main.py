import logging

import dotenv

from app import run

dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO)


def main():
    run()


if __name__ == '__main__':
    main()
