import json
import sqlite3
from models.entry import Entry
from models.mood import Mood

def get_all_entries():
    """function to fetch all records from the entries table"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        # Write the SQL query to grab to desired information
        db_cursor.execute("""
        SELECT
            e.id,
            e.date,
            e.entry,
            e.concept,
            e.moodId,
            m.label
        FROM entries AS e
        JOIN moods AS m
        ON e.moodId = m.id
        """)
        # Initialize empty list to hold all entries representations
        entries = []
        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()
        # Iterate list of data returned from DB
        for row in dataset:
            # Create an entries instance from the current row.
            # DB files are in exact order of the parameters defined
            # in the Entries class.
            entry = Entry(row['id'], row['date'], row['entry'],
                            row['concept'], row['moodId'])            
            # Create mood instance from the current row.
            mood = Mood(row["id"], row["label"])           
            # Add dict representation of the mood to the entry
            entry.mood = mood.__dict__
            
            # Add dict representation of the entry to the list
            entries.append(entry.__dict__)
            
      
        # User 'json' package to properly serialize list as JSON
        return json.dumps(entries)

def get_single_entry(id):
    """FN to fetch a single entry based on provided id"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        entries = []
        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            e.id,
            e.date,
            e.entry,
            e.concept,
            e.moodId,
            m.label
        FROM entries AS e
        JOIN moods AS m
        ON e.moodId = m.id
        WHERE e.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an entries instance from the current row
        entry = Entry(data['id'], data['date'], data['entry'],
                            data['concept'], data['moodId'])        
        mood = Mood(data["id"], data["label"])        
        # Add dict representation of the mood to the entry
        entry.mood = mood.__dict__        
        # Add dict representation of the entry to the list
        entries.append(entry.__dict__)

        return json.dumps(entry.__dict__)

def delete_entry(id):
    """FN to delete an entry record based on the id as an argument"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM entries
        WHERE id = ?
        """, (id, ))

def search_entries(searchedTerm):
    """FN to search the entries records for LIKE and CONTAIN"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT *
        FROM entries AS e
        WHERE e.entry = ?
            OR e.concept = ?
        """, (id, ))
        
        
        
        # LIKE "%{searchedTerm}%"
        # LIKE term "%{searchedTerm}%"
        
        # Initialize an empty list to hold all entries representations
        entries = []
        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()
        # Iterate the list of data returned from the DB
        for row in dataset:
            entry = Entry(row["id"], row["date"], row["entry"],
                          row["concept"], row["moodId"])
        # Add dictionary represetnation of the entry to the list
        entries.append(entry.__dict__)
    return json.dumps(entries)

def update_entry(id, updated_entry_value):
    """FN to UPDATE a single entry based on the supplied id"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE entries
        SET 
            date = ?,
            entry = ?,
            concept = ?,
            moodId = ?
        WHERE id = ? 
        """, (updated_entry_value['date'], updated_entry_value['entry'],
              updated_entry_value['concept'], updated_entry_value['moodId'], id, ))
        
        rows_affected = db_cursor.rowcount
        
    if rows_affected == 0:
        return False
    else:
        return True

def create_entry(new_entry):
    """FN to create a new entry for the entries table"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO entries
            ( date, entry, concept, moodId )
        VALUES
            ( ?, ?, ?, ?);
        """, (new_entry['date'], new_entry['entry'],
              new_entry['concept'], new_entry['moodId'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the entry dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_entry['id'] = id


    return json.dumps(new_entry)
