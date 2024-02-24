import argparse

from database import DatabaseManager
from preferences import UserPreferences

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some arguments.')
    parser.add_argument('--prompt', type=str, help='A prompt for the script')
    parser.add_argument('--persona', type=str, help='A persona for the script')
    parser.add_argument('--user', type=str, help='A database for storing preferences')
    parser.add_argument('--iterations', type=int, help='Number of iterations to run the script')
    args = parser.parse_args()

    prompt = args.prompt
    persona = args.persona
    user = args.user
    iterations = args.iterations

    try:

        db = DatabaseManager('{user}.db')
        db.create_database()
        db.initialize_tables()
        db.populate_tables()

        preferences = UserPreferences(db, persona)

        for i in range(iterations):

            preferences.fetch_and_process_prompt()
            preferences.print_waiting_images()
            preferences.process_waiting_images()

            print(db.fetch_random_qualities())

    except Exception as e:

        print(e)

        db.delete_tables()
        db.delete_database()

    db.delete_tables()
    db.delete_database()

