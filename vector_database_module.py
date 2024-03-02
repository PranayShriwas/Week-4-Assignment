# import sqlite3

# # Initialize database
# conn = sqlite3.connect('conversation.db')
# c = conn.cursor()

# # Create table
# c.execute('''CREATE TABLE IF NOT EXISTS conversations
#              (user_input TEXT, response TEXT, sentiment TEXT)''')

# def save_user_input(user_input):
#     c.execute("INSERT INTO conversations (user_input) VALUES (?)", (user_input,))
#     conn.commit()

# def save_response(response, sentiment):
#     c.execute("UPDATE conversations SET response=?, sentiment=? WHERE rowid=(SELECT MAX(rowid) FROM conversations)", (response, sentiment))
#     conn.commit()

# def close_connection():
#     conn.close()

# # vector_database_module.py

# #Psycopg2

import psycopg2
from flask import g

class DatabaseError(Exception):
    pass

def save_user_input(db, user_input):
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO conversations (user_input) VALUES (%s);", (user_input,))
        db.commit()
    except psycopg2.Error as e:
        # Handle database error gracefully
        db.rollback()
        raise DatabaseError(f"Error saving user input to database: {e}")
    finally:
        cursor.close()

def save_response(db, response, sentiment):
    cursor = db.cursor()
    try:
        cursor.execute("UPDATE conversations SET response=%s, sentiment=%s WHERE rowid=(SELECT MAX(rowid) FROM conversations)", (response, sentiment))
        db.commit()
    except psycopg2.Error as e:
        # Handle database error gracefully
        db.rollback()
        raise DatabaseError(f"Error saving response to database: {e}")
    finally:
        cursor.close()
