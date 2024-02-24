import argparse

from database import DatabaseManager
from preferences import UserPreferences

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some arguments.')
    parser.add_argument('--prompt', type=str, help='A prompt for the script')
    parser.add_argument('--user', type=str, help='A database for storing preferences')
    args = parser.parse_args()

    prompt = args.prompt
    user = args.user

    try:

        db = DatabaseManager('{user}.db')
        db.create_database()
        db.initialize_tables()
        db.populate_tables()

        preferences = UserPreferences(db)
        preferences.fetch_and_process_prompt()
        preferences.process_waiting_images()

        print(db.fetch_random_qualities())

    except Exception as e:

        print(e)

        db.delete_tables()
        db.delete_database()

    db.delete_tables()
    db.delete_database()

