# todo.py
import logging
import sys
from classes import User
from funcs import get_user_info, welcome, menu_logic

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    setup_logging()
    logging.info("Starting PyPlanner")

    try:
        user = User()
        get_user_info(user)
        welcome(user)
        menu_logic(user)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)

    logging.info("PyPlanner finished successfully")

if __name__ == "__main__":
    main()
