''' Main module. '''
import sys
import os
import time
import pyodbc
from faker import Faker

fake = Faker()

CONNECTION_STRING = 'DRIVER={{PostgreSQL Unicode}};SERVER={server};DATABASE={database};UID={username};PWD={password};'

SQL_CREATE_TABLE = '''
    CREATE TABLE users (
        id INT,
        name VARCHAR(50),
        city VARCHAR(50)
    )
'''

SQL_INSERT_DATA = 'INSERT INTO users (id, name, city) VALUES (?, ?, ?)'

default_count = 10

data = []


# def get_data():
#     count = default_count
#     if len(sys.argv) != 1:
#         count = int(sys.argv[1])
#     for i in range(count):
#         name = fake.name().encode('utf-8')
#         city = fake.city().encode('utf-8')
#         data_set = (i, name, city)
#         data.append(data_set)
#     return data

def get_data():
    count = default_count
    if os.getenv('DATA_COUNT'):
        count = int(os.getenv('DATA_COUNT'))
    for i in range(count):
        name = fake.name().encode('utf-8')
        city = fake.city().encode('utf-8')
        data_set = (i, name, city)
        data.append(data_set)
    return data


def connect_db():
    ''' Connect to database. '''
    print('Establishing pg database connection.')
    connection_str = CONNECTION_STRING.format(
        server=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        username=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD']
    )

    return pyodbc.connect(connection_str, timeout=300)


def setup_table(cur):
    ''' Create table and populate data. '''
    print('Create a new table for users.')
    cur.execute(SQL_CREATE_TABLE)
    cur.commit()

    print('Populate users data.')
    for row in data:
        cur.execute(SQL_INSERT_DATA, row)
    cur.commit()


def fetch_data(cur):
    ''' Fetch all data from the table. '''
    print('List of data.')
    cur.execute('SELECT * FROM users')

    return cur.fetchall()


def display_data(rows):
    ''' Print rows in the console. '''
    template = '{:<5} {:<15} {:<10}'
    print(template.format('ID', 'NAME', 'CITY'))
    print('-' * 32)
    for row in rows:
        print(template.format(row.id, row.name, row.city))


def main():
    ''' App entrypoint. '''
    time.sleep(5)  # Wait for database server to fully spawn.
    conn = connect_db()
    cur = conn.cursor()
    get_data()

    setup_table(cur)
    rows = fetch_data(cur)
    display_data(rows)

    print('Closing the connection.')
    cur.close()
    conn.close()
    sys.exit(0)


main()
