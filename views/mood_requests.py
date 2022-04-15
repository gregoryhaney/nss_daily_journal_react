import json
import sqlite3
from models.mood import Mood


def get_all_moods():
    """function to fetch all records from the moods table"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        # Write the SQL query to grab to desired information
        db_cursor.execute("""
        SELECT
            m.id,
            m.label
        FROM moods AS m
        """)
        
        # Initialize empty list to hold all moods representations
        moods = []
        
        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()
        
        # Iterate list of data returned from DB
        for row in dataset:
            
            # Create a moods instance from the current row.
            # DB files are in exact order of the parameters defined
            # in the Entries class.
            mood = Mood(row['id'], row['label'])
            
            # Add dict representation of the mood to the list
            moods.append(mood.__dict__)
        
        # User 'json' package to properly serialize list as JSON
        return json.dumps(moods)

def get_single_mood(id):
    """FN to fetch a single entry based on provided id"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            m.id,
            m.label
        FROM moods AS m
        WHERE m.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an entries instance from the current row
        mood = Mood(data['id'], data['label'])

        return json.dumps(mood.__dict__)
        