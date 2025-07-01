import sqlite3

class DataHandler():

    def __init__(self):

        self.db_path = "./data/app.db"
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

        self.create_tables()
        # Insert data
        # self.cursor.execute('''
        # INSERT INTO users (name, email) VALUES (?, ?)
        # ''', ("John Doe", "john@example.com"))

        # Commit changes and close the connection
        self.connection.commit()
        self.connection.close()

        # Query the database
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        #self.cursor.execute("SELECT * FROM users")
        print(self.cursor.fetchall())
        self.connection.close()

    def create_tables(self):
        self.cursor.execute('''
            -- Table: instances
            CREATE TABLE IF NOT EXISTS instances (
                id INTEGER PRIMARY KEY,
                dimension INTEGER,
                path TEXT,
                body TEXT,
                absolute_best REAL
            );
        ''')
        self.cursor.execute('''
            -- Table: configurations
            CREATE TABLE IF NOT EXISTS configurations (
                id INTEGER PRIMARY KEY,
                name TEXT,
                created_at DATETIME,
                parameters TEXT -- Use TEXT to store JSON in SQLite
            );
        ''')
        self.cursor.execute(
            '''
            -- Table: executions
            CREATE TABLE IF NOT EXISTS executions (
                id INTEGER PRIMARY KEY,
                instance_id INTEGER NOT NULL,
                config_id INTEGER NOT NULL,
                best REAL,
                best_individual TEXT,
                metrics TEXT,
                FOREIGN KEY (instance_id) REFERENCES instances(id) ON DELETE CASCADE,
                FOREIGN KEY (config_id) REFERENCES configurations(id) ON DELETE CASCADE
            );
            '''
        )

    

    def get_all_instances(self):
        # all files that have .atsp extension in ./instances/data
        import os
        instances_path = "./data/instances/"
        all_files = [f for f in os.listdir(instances_path) if os.path.isfile(os.path.join(instances_path, f))]
        print(all_files)
        return all_files
    

if __name__ == "__main__":
    x = DataHandler()
    x.get_all_instances()