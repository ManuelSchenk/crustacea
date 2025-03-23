import sqlite3
from pathlib import Path

class StorageContext:
    def __init__(self):
        """
        This Class provide access to the sqlite database where all statistics from the training were stored
        """
        self.db_path = Path(__file__).parents[1] / "db" / "crust.db"

    def __enter__(self):
        # Create a connection to the database
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        return self
    
    def _create_table(self):
        """Create the table if it doesn't already exist. Normally not needed"""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS score_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            char_counter INTEGER,
            error_counter INTEGER,
            "error_rate" REAL,
            "char_min" REAL,
            score INTEGER
        );
        """
        self.cursor.execute(create_table_sql)
        self.connection.commit()

    def query(self, query, params=None):
        """Execute a query on the sqlite DB with parameters if provided."""
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def insert_result(self, filename, char_counter, error_counter, error_rate, char_per_min, score):
        """
        Insert a new row into the score_table after a training was finished
        
        Returns:
            int: The row id of the inserted row.
        """
        sql = '''
        INSERT INTO score_table (filename, char_counter, error_counter, "error_rate", "char_min", score)
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        self.cursor.execute(sql, (filename, char_counter, error_counter, error_rate, char_per_min, score))
        self.connection.commit()
        return self.cursor.lastrowid

    def __exit__(self, exc_type, exc_value, traceback):
        # Ensure the connection is closed
        self.connection.close()



if __name__ == "__main__":
    with StorageContext() as db:
        # this creates the crust.db file if not already existing
        db._create_table()

        # Insert an example row
        row_id = db.insert_result("initial", 0, 0, 0.0, 0.0, 0)
        print("Inserted row id:", row_id)
        
        # Query by filename
        query = 'SELECT * FROM score_table WHERE filename = "initial"'
        rows = db.query(query)
        print("Rows with filename 'initial':")
        for row in rows:
            print(row)
