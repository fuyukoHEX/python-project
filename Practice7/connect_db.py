import psycopg2
import csv

DB_PARAMS = {
    "host": "localhost",
    "database": "phonebook_db",
    "user": "postgres",
    "password": "Pro777aka"
}

def execute_query(query, params=None, fetch=False):
    try:
        with psycopg2.connect(**DB_PARAMS) as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                if fetch:
                    return cur.fetchall()
                return cur.rowcount
    except Exception as e:
        print(f"Connection error: {e}")
        return None

def create_table():
    execute_query("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    """)

def add_from_console():
    name = input("Name: ")
    phone = input("Phone: ")
    execute_query("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)", (name, phone))
    print(f"Contact {name} added.")

def add_from_csv():
    filename = input("CSV filename: ")
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            added_count = 0
            for row in reader:
                if len(row) >= 2:
                    execute_query("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)", (row[0], row[1]))
                    added_count += 1
            print(f"Added {added_count} contacts.")
    except FileNotFoundError:
        print("File not found.")

def get_users():
    print("\nSearch\n1.All\n2.By name\n3.By number")
    choice = input("Choice: ")
    
    if choice == "1":
        res = execute_query("SELECT * FROM phonebook ORDER BY id ASC", fetch=True)
    elif choice == "2":
        name = input("Name: ")
        res = execute_query("SELECT * FROM phonebook WHERE first_name LIKE %s", (f'%{name}%',), fetch=True)
    elif choice == "3":
        phone = input("Number: ")
        res = execute_query("SELECT * FROM phonebook WHERE phone LIKE %s", (f'%{phone}%',), fetch=True)
    else:
        print("Invalid operation")
        return

    if not res:
        print("Not found")
    else:
        print("\nResult:")
        for row in res:
            print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")

def update_user():
    name = input("Name to update: ")
    new_phone = input("New number: ")
    count = execute_query("UPDATE phonebook SET phone = %s WHERE first_name = %s", (new_phone, name))
    print(f"Number for {name} updated." if count else f"Contact {name} not found.")

def delete_user():
    name = input("Name to delete: ")
    if input(f"Delete {name}? (y/n): ").lower() == 'y':
        count = execute_query("DELETE FROM phonebook WHERE first_name = %s", (name,))
        print(f"Contact {name} deleted." if count else f"Contact {name} not found.")
    else:
        print("Cancelled.")

def main_menu():
    create_table()
    while True:
        print("\nMenu:\n1.Add\n2.Load from CSV\n3.Show/Search\n4.Update\n5.Delete\n0.Exit")
        choice = input("Choice: ")
        if choice == "1": add_from_console()
        elif choice == "2": add_from_csv()
        elif choice == "3": get_users()
        elif choice == "4": update_user()
        elif choice == "5": delete_user()
        elif choice == "0":
            print("Finished")
            break
        else:
            print("Input error")

if __name__ == "__main__":
    main_menu()