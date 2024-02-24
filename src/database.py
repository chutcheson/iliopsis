import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name):
        self.db_path = os.path.join('../data', db_name)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def create_database(self):
        if os.path.exists(self.db_path):
            raise FileExistsError(f"Database '{self.db_path}' already exists.")
        
        # If the file does not exist, connect to create the database file
        conn = sqlite3.connect(self.db_path)
        print(f"Database '{self.db_path}' created successfully.")
        conn.close()

    def initialize_tables(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS positive_qualities
                       (positive_quality TEXT)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS negative_qualities
                       (negative_quality TEXT)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS prompts 
                       (prompt TEXT, success INTEGER)''')  
        cur.execute('''CREATE TABLE IF NOT EXISTS images
                       (uuid TEXT, prompt TEXT)''')
        print("Tables initialized successfully.")
        conn.commit()
        conn.close()

    def populate_tables(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("INSERT INTO positive_qualities (positive_quality) VALUES ('make science look cool')")
        cur.execute("INSERT INTO negative_qualities (negative_quality) VALUES ('be boring')")
        cur.execute("INSERT INTO prompts (prompt, success) VALUES ('a brown tabby cat working at an IBM mainframe supercomputer in the style of a Japanese woodblock print', 1)")
        print("Tables populated successfully.")
        conn.commit()
        conn.close()

    def insert_positive_quality(self, positive_quality):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        # Check if the value already exists
        cur.execute("SELECT * FROM positive_qualities WHERE positive_quality = ?", (positive_quality,))
        if cur.fetchone():
            conn.close()
            return False 
        else:
            cur.execute("INSERT INTO positive_qualities (positive_quality) VALUES (?)", (positive_quality,))
            conn.commit()
            conn.close()
            return True 

    def insert_negative_quality(self, negative_quality):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        # Check if the value already exists
        cur.execute("SELECT * FROM negative_qualities WHERE negative_quality = ?", (negative_quality,))
        if cur.fetchone():
            conn.close()
            return False  
        else:
            cur.execute("INSERT INTO negative_qualities (negative_quality) VALUES (?)", (negative_quality,))
            conn.commit()
            conn.close()
            return True

    def insert_prompt(self, prompt, success):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        success_int = 1 if success else 0
        cur.execute("SELECT * FROM prompts WHERE prompt = ?", (prompt,))
        if cur.fetchone():
            conn.close()
            return False  
        else:
            cur.execute("INSERT INTO prompts (prompt, success) VALUES (?, ?)", (prompt, success_int))
            conn.commit()
            conn.close()
            return True

    def insert_image(self, uuid, prompt):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM images WHERE uuid = ?", (uuid,))
        if cur.fetchone():
            conn.close()
            return False
        else:
            cur.execute("INSERT INTO images (uuid, prompt) VALUES (?, ?)", (uuid, prompt))
            conn.commit()
            conn.close()
            return True

    def fetch_random_qualities(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM positive_qualities ORDER BY RANDOM() LIMIT 10")
        positives = cur.fetchall()
        cur.execute("SELECT * FROM negative_qualities ORDER BY RANDOM() LIMIT 10")
        negatives = cur.fetchall()
        conn.close()
        return positives, negatives

    def fetch_random_prompt(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM prompts WHERE success = 1 ORDER BY RANDOM() LIMIT 1")
        prompt = cur.fetchone()
        conn.close()
        return prompt

    def fetch_image(self, uuid):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM images WHERE uuid = ?", (uuid,))
        image = cur.fetchone()
        conn.close()
        return image

    def delete_tables(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS positive_qualities")
        cur.execute("DROP TABLE IF EXISTS negative_qualities")
        cur.execute("DROP TABLE IF EXISTS prompts")
        print("Tables deleted successfully.")
        conn.commit()
        conn.close()

    def delete_database(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
            print(f"Database '{self.db_path}' has been deleted.")
        else:
            print("Database does not exist or was already deleted.")

if __name__ == "__main__":
    db = DatabaseManager('iris.db')
    db.create_database()
    db.initialize_tables()
    db.populate_tables()
    print(db.fetch_random_qualities())
    print(db.fetch_random_prompt())
    db.delete_tables()
    db.delete_database()
