from connect import get_connection

def search_contact():
    pattern = input("Enter search pattern: ")
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM search_contacts(%s);", (pattern,))
        print("Search Results:", cur.fetchall())

def upsert_contact():
    name = input("Enter contact name: ")
    phone = input("Enter contact phone: ")
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("CALL upsert_contact(%s, %s);", (name, phone))
        print("Contact saved successfully.")

def bulk_insert():
    names = [n.strip() for n in input("Enter names separated by comma: ").split(',')]
    phones = [p.strip() for p in input("Enter phones separated by comma: ").split(',')]
    
    if len(names) != len(phones):
        print("Error: Name and phone counts must match.")
        return

    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("CALL bulk_insert_contacts(%s, %s, %s);", (names, phones, []))
        failed = cur.fetchone()[0]
        print("Failed to insert records:", failed if failed else "None")

def paginate_contacts():
    limit = int(input("Enter limit (rows per page): "))
    offset = int(input("Enter offset (rows to skip): "))
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (limit, offset))
        print("Paginated Results:", cur.fetchall())

def delete_contact():
    identifier = input("Enter name or phone to delete: ")
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("CALL delete_contact(%s);", (identifier,))
        print("Contact deleted successfully.")

def main():
    actions = {
        '1': search_contact,
        '2': upsert_contact,
        '3': bulk_insert,
        '4': paginate_contacts,
        '5': delete_contact
    }
    
    while True:
        print("\n--- PhoneBook Menu ---")
        choice = input("1: Search | 2: Upsert | 3: Bulk Insert | 4: Paginate | 5: Delete | 0: Exit\nChoose: ")
        
        if choice == '0':
            print("Exiting...")
            break
        elif choice in actions:
            try:
                actions[choice]()
            except Exception as e:
                print(f"Database error: {e}")
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()