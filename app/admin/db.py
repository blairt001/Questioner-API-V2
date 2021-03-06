"""
    Initializes a connection to the db
"""
import os
import sys
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash  # for password hashing
from dotenv import load_dotenv


def init_db(DB_URL=None):
    """
        Initialize db connection
    """
    try:
        conn, cursor = connect_to_db()
        create_db_query = drop_table_if_exists() + set_up_tables()
        i = 0
        while i != len(create_db_query):
            query = create_db_query[i]
            cursor.execute(query)
            conn.commit()
            i += 1
        print("--"*50)
        conn.close()

    except Exception as error:
        print("\nQuery not executed : {} \n".format(error))


def set_up_tables():
    """
        Queries run to set up and create tables
    """
    table_users = """
    CREATE TABLE users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR (24) NOT NULL UNIQUE,
        firstname VARCHAR (24) NOT NULL,
        lastname VARCHAR (24) NOT NULL,
        phone INTEGER NOT NULL,
        email VARCHAR (30) NOT NULL UNIQUE,
        password VARCHAR (128) NOT NULL,
        admin BOOLEAN
    )"""

    table_meetups = """
    CREATE TABLE meetups (
        meetup_id SERIAL PRIMARY KEY,
        topic VARCHAR (24) NOT NULL,
        happenningon TIMESTAMP,
        meetup_location VARCHAR (24) NOT NULL,
        meetup_images VARCHAR (24) NOT NULL,
        meetup_tags VARCHAR,
        created_at TIMESTAMP
    )"""

    table_questions = """
    CREATE TABLE questions (
        question_id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        meetup_id INTEGER NOT NULL,
        title VARCHAR (50) NOT NULL,
        body VARCHAR (200) NOT NULL,
        votes INTEGER NOT NULL,
        comment VARCHAR,
        created_at TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (meetup_id) REFERENCES meetups(meetup_id) ON DELETE CASCADE
    )"""

    table_comments = """
    CREATE TABLE comments (
        comment_id SERIAL PRIMARY KEY,
        user_id INTEGER,
        question_id INTEGER NOT NULL,
        title VARCHAR,
        body VARCHAR,
        comment VARCHAR,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE CASCADE
    )"""

    table_rsvps = """
    CREATE TABLE rsvps (
        rsvp_id SERIAL PRIMARY KEY,
        meetup_id INTEGER,
        user_id INTEGER,
        meetup_topic VARCHAR,
        rsvp VARCHAR,
        FOREIGN KEY (meetup_id) REFERENCES meetups(meetup_id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    )"""

    table_votes = """
     CREATE TABLE votes (
        user_id INTEGER,
        question_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE CASCADE
    )"""
    table_tokens = """
    CREATE TABLE blacklist_tokens (
        token_id SERIAL PRIMARY KEY,
        token VARCHAR
    )"""

    # create a super user admin with hashed password
    password = generate_password_hash('Andela2019')
    create_admin_query = """
    INSERT INTO users(username, firstname, lastname, phone, email, password, admin) VALUES(
        '{}', '{}', '{}', '{}', '{}', '{}', '{}'
    )""".format('admin', 'Tony', 'Blair', '0715096908', 'admin@gmail.com', password, True)

    return [table_users, table_meetups,
            table_questions, table_comments,
            table_rsvps, create_admin_query,
            table_votes, table_tokens]


def drop_table_if_exists():
    """
        Removes all tables on app restart
    """
    drop_users_table = """
    DROP TABLE IF EXISTS users CASCADE"""

    drop_meetups_table = """
    DROP TABLE IF EXISTS meetups CASCADE"""

    drop_questions_table = """
    DROP TABLE IF EXISTS questions CASCADE"""

    drop_comments_table = """
    DROP TABLE IF EXISTS comments CASCADE"""

    drop_rsvps_table = """
    DROP TABLE IF EXISTS rsvps CASCADE"""

    drop_votes_table_ = """
    DROP TABLE IF EXISTS votes CASCADE"""

    drop_blacklist_tokens_table_ = """
    DROP TABLE IF EXISTS blacklist_tokens CASCADE"""

    return [drop_comments_table, drop_meetups_table,
            drop_questions_table, drop_users_table,
            drop_rsvps_table, drop_votes_table_,
            drop_blacklist_tokens_table_]


def connect_to_db(query=None, DB_URL=None):
    """
        Initiates a connection to the db and executes a query
    """
    conn = None
    cursor = None
    if DB_URL is None:
        DB_URL = os.getenv('DATABASE_URL')

    try:
        # connect to db
        conn = psycopg2.connect(DB_URL)
        print("\n\nConnected {}\n".format(conn.get_dsn_parameters()))
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        if query:
            # Execute query
            cursor.execute(query)
            # Commit changes
            conn.commit()

    except(Exception,
           psycopg2.DatabaseError,
           psycopg2.ProgrammingError) as error:
        print("DB ERROR: {}".format(error))

    return conn, cursor


def query_data_from_db(query):
    """
        Handles INSERT queries
    """
    try:
        conn = connect_to_db(query)[0]
        # After successful INSERT query
        conn.close()
    except psycopg2.Error as error:
        sys.exit(1)


def select_data_from_db(query):
    """
        Handles SELECT queries
    """
    rows = None
    conn, cursor = connect_to_db(query)
    if conn:
        # Retrieve SELECT query results from db
        rows = cursor.fetchall()
        conn.close()

    return rows

# initialize the db operations now
if __name__ == '__main__':
    init_db()
    connect_to_db()
