import psycopg2
import csv
import os

try:
    conn = psycopg2.connect(
        host="localhost",
        database="phonebook_db",
        user="postgres",
        password="Pro777aka"
    )
    cur = conn.cursor()
    print("Connection successful.")
except Exception as e:
    print(f"Connection error: {e}")
    exit()

def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    """)
    conn.commit()

def add_from_console():
    name = input("Name: ")
    phone = input("Phone: ")
    
    cur.execute(
        "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
        (name, phone)
    )
    conn.commit()
    print(f"Contact {name} added.")

def add_from_csv():
    filename = input("CSV filename: ")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, filename)
    
    try:
        with open(full_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            try:
                next(reader)
            except StopIteration:
                print("Error: file is empty.")
                return

            added_count = 0
            for row in reader:
                if len(row) >= 2:
                    cur.execute(
                        "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
                        (row[0], row[1])
                    )
                    added_count += 1
            conn.commit()
            print(f"Added {added_count} contacts.")
    except FileNotFoundError:
        print("File not found.")

def get_users():
    print("\nSearch")
    print("1.All")
    print("2.By name")
    print("3.By number")
    
    choice = input("Choice: ")
    
    if choice == "1":
        cur.execute("SELECT * FROM phonebook ORDER BY id ASC")
    elif choice == "2":
        name = input("Name: ")
        cur.execute("SELECT * FROM phonebook WHERE first_name LIKE %s", (f'%{name}%',))
    elif choice == "3":
        phone = input("Number: ")
        cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s", (f'%{phone}%',))
    else:
        print("Invalid operation")
        return

    rows = cur.fetchall()
    
    if not rows:
        print("Not found")
    else:
        print("\nResult:")
        for row in rows:
            print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")

def update_user():
    name = input("Name to update: ")
    new_phone = input("New number: ")
    
    cur.execute(
        "UPDATE phonebook SET phone = %s WHERE first_name = %s",
        (new_phone, name)
    )
    
    if cur.rowcount > 0:
        conn.commit()
        print(f"Number for {name} updated.")
    else:
        print(f"Contact {name} not found.")

def delete_user():
    name = input("Name to delete: ")
    
    confirm = input(f"Delete {name}? (y/n): ")
    if confirm.lower() == 'y':
        cur.execute("DELETE FROM phonebook WHERE first_name = %s", (name,))
        
        if cur.rowcount > 0:
            conn.commit()
            print(f"Contact {name} deleted.")
        else:
            print(f"Contact {name} not found.")
    else:
        print("Cancelled.")

def main_menu():
    create_table()
    
    while True:
        print("\nMenu:")
        print("1.Add")
        print("2.Load from CSV")
        print("3.Show/Search")
        print("4.Update")
        print("5.Delete")
        print("0.Exit")

        choice = input("Choice: ")

        if choice == "1":
            add_from_console()
        elif choice == "2":
            add_from_csv()
        elif choice == "3":
            get_users()
        elif choice == "4":
            update_user()
        elif choice == "5":
            delete_user()
        elif choice == "0":
            print("Finished")
            break
        else:
            print("Input error")

if __name__ == "__main__":
    main_menu()
    
    if cur:
        cur.close()
    if conn:
        conn.close()