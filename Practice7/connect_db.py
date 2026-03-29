import csv
from connect import get_connection

conn = get_connection()
cur = conn.cursor()

def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name TEXT,
            phone TEXT
        )
    """)

def add_from_console():
    name = input("Name: ")
    phone = input("Phone: ")
    cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)", (name, phone))
    print("Contact added.")

def add_from_csv():
    filename = input("CSV filename: ")
    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)", (row[0], row[1]))
    print("Contacts from CSV added.")

def get_users():
    print("1. All | 2. By name | 3. By number")
    choice = input("Choice: ")
    
    if choice == "1":
        cur.execute("SELECT * FROM phonebook ORDER BY id ASC")
    elif choice == "2":
        name = input("Name: ")
        cur.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s", ('%' + name + '%',))
    elif choice == "3":
        phone = input("Number: ")
        cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s", (phone + '%',))
        
    for row in cur.fetchall():
        print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")

def update_user():
    print("1. Update name | 2. Update phone")
    choice = input("Choice: ")
    
    if choice == "1":
        old_name = input("Name to update: ")
        new_name = input("New name: ")
        cur.execute("UPDATE phonebook SET first_name = %s WHERE first_name = %s", (new_name, old_name))
    elif choice == "2":
        name = input("Name to update: ")
        new_phone = input("New number: ")
        cur.execute("UPDATE phonebook SET phone = %s WHERE first_name = %s", (new_phone, name))
    
    print("Updated.")

def delete_user():
    print("1. By name | 2. By number")
    choice = input("Choice: ")
    
    if choice == "1":
        name = input("Name to delete: ")
        cur.execute("DELETE FROM phonebook WHERE first_name = %s", (name,))
    elif choice == "2":
        phone = input("Number to delete: ")
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
        
    print("Deleted.")

def main_menu():
    create_table()
    while True:
        print("\n1.Add | 2.CSV | 3.Search | 4.Update | 5.Delete | 0.Exit")
        choice = input("Choice: ")
        
        if choice == "1": add_from_console()
        elif choice == "2": add_from_csv()
        elif choice == "3": get_users()
        elif choice == "4": update_user()
        elif choice == "5": delete_user()
        elif choice == "0": break

if __name__ == "__main__":
    main_menu()