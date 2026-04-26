"""
TSIS1 - PhoneBook: Extended Contact Manager
Run: python phonebook.py

IMPORTANT: Before running, execute the following in PostgreSQL:
  1) schema.sql     - Create tables
  2) procedures.sql - Create stored procedures and functions
"""

import json
import csv
from connect import get_connection


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def print_contacts(rows, headers):
    """Prints a list of contacts in a formatted table."""
    if not rows:
        print("  (no records found)")
        return
    print("  " + " | ".join(headers))
    print("  " + "-" * 65)
    for row in rows:
        # Convert None to empty string for clean output
        values = [str(v) if v is not None else "" for v in row]
        print("  " + " | ".join(values))


def get_all_groups():
    """Returns a list of all groups from the database."""
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT id, name FROM groups ORDER BY name")
        return cur.fetchall()


# ============================================================
# 3.1 - ADD CONTACT
# ============================================================

def add_contact():
    """Adds a new contact with email, birthday, and group."""
    print("\n--- Add New Contact ---")

    name = input("Name: ").strip()
    if not name:
        print("Error: Name cannot be empty!")
        return

    email = input("Email (Enter to skip): ").strip() or None
    birthday = input("Birthday (YYYY-MM-DD, Enter to skip): ").strip() or None

    # Display groups
    groups = get_all_groups()
    print("Groups:")
    for g in groups:
        print(f"  {g[0]}. {g[1]}")
    group_input = input("Group ID (Enter to skip): ").strip()
    group_id = int(group_input) if group_input.isdigit() else None

    phone = input("Phone Number: ").strip()
    phone_type = input("Phone Type (home / work / mobile): ").strip().lower()
    if phone_type not in ('home', 'work', 'mobile'):
        phone_type = 'mobile'

    try:
        with get_connection() as conn, conn.cursor() as cur:
            # Insert contact
            cur.execute("""
                INSERT INTO contacts (name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (name, email, birthday, group_id))
            contact_id = cur.fetchone()[0]

            # Insert phone
            cur.execute("""
                INSERT INTO phones (contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (contact_id, phone, phone_type))

        print(f"Contact '{name}' successfully added!")
    except Exception as e:
        print(f"Error: {e}")


# ============================================================
# 3.2 - SEARCH BY ALL FIELDS
# ============================================================

def search_contact():
    """Searches contacts by name, email, or phone using a DB function."""
    print("\n--- Search Contact ---")
    query = input("Enter search term (name / email / phone): ").strip()

    try:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute("SELECT * FROM search_contacts(%s)", (query,))
            rows = cur.fetchall()
        print_contacts(rows, ["ID", "Name", "Email", "Phone", "Type"])
    except Exception as e:
        print(f"Error: {e}")


# ============================================================
# 3.2 - FILTER BY GROUP
# ============================================================

def filter_by_group():
    """Displays contacts belonging to a specific group."""
    print("\n--- Filter by Group ---")
    groups = get_all_groups()
    print("Available Groups:")
    for g in groups:
        print(f"  {g[0]}. {g[1]}")

    group_input = input("Enter Group ID: ").strip()
    if not group_input.isdigit():
        print("Invalid input!")
        return

    try:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute("""
                SELECT c.id, c.name, c.email, c.birthday, p.phone, p.type
                FROM contacts c
                LEFT JOIN phones p ON p.contact_id = c.id
                WHERE c.group_id = %s
                ORDER BY c.name
            """, (int(group_input),))
            rows = cur.fetchall()
        print_contacts(rows, ["ID", "Name", "Email", "Birthday", "Phone", "Type"])
    except Exception as e:
        print(f"Error: {e}")


# ============================================================
# 3.2 - SEARCH BY EMAIL
# ============================================================

def search_by_email():
    """Searches contacts by partial email address."""
    print("\n--- Search by Email ---")
    email_query = input("Email part (e.g., 'gmail'): ").strip()

    try:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute("""
                SELECT c.id, c.name, c.email, p.phone
                FROM contacts c
                LEFT JOIN phones p ON p.contact_id = c.id
                WHERE c.email ILIKE %s
                ORDER BY c.name
            """, (f'%{email_query}%',))
            rows = cur.fetchall()
        print_contacts(rows, ["ID", "Name", "Email", "Phone"])
    except Exception as e:
        print(f"Error: {e}")


# ============================================================
# 3.2 - SORTED VIEW
# ============================================================

def show_all_sorted():
    """Displays all contacts with a user-selected sorting method."""
    print("\n--- All Contacts ---")
    print("Sort by: 1. Name  2. Birthday  3. Date Added")
    sort_choice = input("Select (1/2/3): ").strip()

    sort_column = {
        '1': 'c.name',
        '2': 'c.birthday',
        '3': 'c.created_at'
    }.get(sort_choice, 'c.name')

    try:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(f"""
                SELECT c.id, c.name, c.email, c.birthday, g.name AS grp, p.phone, p.type
                FROM contacts c
                LEFT JOIN groups g ON g.id = c.group_id
                LEFT JOIN phones p ON p.contact_id = c.id
                ORDER BY {sort_column}
            """)
            rows = cur.fetchall()
        print_contacts(rows, ["ID", "Name", "Email", "Birthday", "Group", "Phone", "Type"])
    except Exception as e:
        print(f"Error: {e}")


# ============================================================
# 3.2 - PAGINATION (next / prev / quit)
# ============================================================

def paginate_contacts():
    """Provides a paginated view of contacts."""
    print("\n--- Paginated View ---")
    page_size = 3
    offset = 0

    while True:
        try:
            with get_connection() as conn, conn.cursor() as cur:
                cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (page_size, offset))
                rows = cur.fetchall()

            if not rows and offset == 0:
                print("  (No contacts found)")
                break

            print(f"\n  Page (Records {offset + 1} - {offset + len(rows)}):")
            print_contacts(rows, ["ID", "Name", "Email", "Birthday", "Group"])

            is_last_page = len(rows) < page_size

            if is_last_page:
                command = input("\n  [prev] back | [quit] exit: ").strip().lower()
            else:
                command = input("\n  [next] forward | [prev] back | [quit] exit: ").strip().lower()

            if command == 'next' and not is_last_page:
                offset += page_size
            elif command == 'prev' and offset > 0:
                offset -= page_size
            elif command == 'quit':
                break
            else:
                print("  (Invalid command)")

        except Exception as e:
            print(f"Error: {e}")
            break


# ============================================================
# 3.3 - EXPORT TO JSON
# ============================================================

def export_to_json():
    """Exports all contacts into a JSON file."""
    print("\n--- Export to JSON ---")
    filename = input("Filename (Enter = contacts_export.json): ").strip() or "contacts_export.json"

    try:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute("""
                SELECT c.id, c.name, c.email,
                       TO_CHAR(c.birthday, 'YYYY-MM-DD') AS birthday,
                       g.name AS grp
                FROM contacts c
                LEFT JOIN groups g ON g.id = c.group_id
                ORDER BY c.name
            """)
            contacts = cur.fetchall()

            result = []
            for contact in contacts:
                contact_id, name, email, birthday, grp = contact

                cur.execute("SELECT phone, type FROM phones WHERE contact_id = %s", (contact_id,))
                phones = [{"phone": row[0], "type": row[1]} for row in cur.fetchall()]

                result.append({
                    "name": name,
                    "email": email,
                    "birthday": birthday,
                    "group": grp,
                    "phones": phones
                })

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"Exported {len(result)} contacts to '{filename}'")
    except Exception as e:
        print(f"Error: {e}")


# ============================================================
# 3.3 - IMPORT FROM JSON
# ============================================================

def import_from_json():
    """Imports contacts from JSON and handles duplicates."""
    print("\n--- Import from JSON ---")
    filename = input("Filename (Enter = contacts_export.json): ").strip() or "contacts_export.json"

    try:
        with open(filename, "r", encoding="utf-8") as f:
            contacts = json.load(f)
    except FileNotFoundError:
        print(f"File '{filename}' not found!")
        return
    except json.JSONDecodeError:
        print("File is corrupted or not valid JSON!")
        return

    added = 0
    skipped = 0

    for contact in contacts:
        name = contact.get("name", "").strip()
        if not name:
            continue

        try:
            with get_connection() as conn, conn.cursor() as cur:
                cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
                existing = cur.fetchone()

                if existing:
                    answer = input(f"  '{name}' already exists. Overwrite? (y/n): ").strip().lower()
                    if answer != 'y':
                        skipped += 1
                        continue
                    contact_id = existing[0]
                    cur.execute("UPDATE contacts SET email=%s, birthday=%s WHERE id=%s", 
                                (contact.get("email"), contact.get("birthday"), contact_id))
                    cur.execute("DELETE FROM phones WHERE contact_id=%s", (contact_id,))
                else:
                    group_name = contact.get("group")
                    group_id = None
                    if group_name:
                        cur.execute("SELECT id FROM groups WHERE name=%s", (group_name,))
                        grp = cur.fetchone()
                        if grp:
                            group_id = grp[0]
                        else:
                            cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (group_name,))
                            group_id = cur.fetchone()[0]

                    cur.execute("INSERT INTO contacts (name, email, birthday, group_id) VALUES (%s, %s, %s, %s) RETURNING id",
                                (name, contact.get("email"), contact.get("birthday"), group_id))
                    contact_id = cur.fetchone()[0]

                for ph in contact.get("phones", []):
                    cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                                (contact_id, ph.get("phone"), ph.get("type")))
            added += 1
        except Exception as e:
            print(f"  Error adding '{name}': {e}")

    print(f"Done: Added {added}, Skipped {skipped}")


# ============================================================
# 3.3 - IMPORT FROM CSV
# ============================================================

def import_from_csv():
    """Imports contacts from a CSV file."""
    print("\n--- Import from CSV ---")
    filename = input("Filename (Enter = contacts.csv): ").strip() or "contacts.csv"

    try:
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except FileNotFoundError:
        print(f"File '{filename}' not found!")
        return

    added = 0
    errors = 0

    for row in rows:
        name = row.get("name", "").strip()
        phone = row.get("phone", "").strip()
        if not name or not phone:
            errors += 1
            continue

        try:
            with get_connection() as conn, conn.cursor() as cur:
                # Group logic
                group_name = row.get("group", "").strip()
                group_id = None
                if group_name:
                    cur.execute("SELECT id FROM groups WHERE name=%s", (group_name,))
                    grp = cur.fetchone()
                    if grp:
                        group_id = grp[0]
                    else:
                        cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (group_name,))
                        group_id = cur.fetchone()[0]

                # Duplicate logic
                cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
                existing = cur.fetchone()

                if existing:
                    contact_id = existing[0]
                else:
                    cur.execute("INSERT INTO contacts (name, email, birthday, group_id) VALUES (%s, %s, %s, %s) RETURNING id",
                                (name, row.get("email") or None, row.get("birthday") or None, group_id))
                    contact_id = cur.fetchone()[0]

                cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                            (contact_id, phone, row.get("phone_type", "mobile").strip().lower()))
            added += 1
        except Exception as e:
            print(f"  Error adding '{name}': {e}")
            errors += 1

    print(f"Done: Added {added}, Errors {errors}")


# ============================================================
# 3.4 - STORED PROCEDURES (Add Phone / Move Group)
# ============================================================

def add_phone():
    """Adds an additional phone to an existing contact using a procedure."""
    print("\n--- Add Phone Number ---")
    name = input("Contact Name: ").strip()
    phone = input("New Phone Number: ").strip()
    ptype = input("Type (home / work / mobile): ").strip().lower() or 'mobile'

    try:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
        print("Phone added!")
    except Exception as e:
        print(f"Error: {e}")


def move_to_group():
    """Moves a contact to another group via procedure."""
    print("\n--- Move to Group ---")
    name = input("Contact Name: ").strip()
    groups = get_all_groups()
    print("Existing Groups:")
    for g in groups:
        print(f"  {g[1]}")
    group_name = input("New Group Name: ").strip()

    try:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute("CALL move_to_group(%s, %s)", (name, group_name))
        print(f"Contact '{name}' moved to group '{group_name}'")
    except Exception as e:
        print(f"Error: {e}")


# ============================================================
# DELETE CONTACT
# ============================================================

def delete_contact():
    """Deletes a contact by name."""
    print("\n--- Delete Contact ---")
    name = input("Name of contact to delete: ").strip()

    confirm = input(f"Are you sure you want to delete '{name}'? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Operation cancelled.")
        return

    try:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute("DELETE FROM contacts WHERE name = %s", (name,))
            if cur.rowcount == 0:
                print(f"Contact '{name}' not found.")
            else:
                print(f"Contact '{name}' deleted.")
    except Exception as e:
        print(f"Error: {e}")


# ============================================================
# MAIN MENU
# ============================================================

def main():
    print("=" * 55)
    print("      TSIS1 - Extended Contact Manager")
    print("=" * 55)

    menu = {
        '1': ("Add Contact", add_contact),
        '2': ("Search (Name/Email/Phone)", search_contact),
        '3': ("Search by Email Part", search_by_email),
        '4': ("Filter by Group", filter_by_group),
        '5': ("All Contacts (Sorted)", show_all_sorted),
        '6': ("Paginated View", paginate_contacts),
        '7': ("Add Phone to Contact", add_phone),
        '8': ("Move to Group", move_to_group),
        '9': ("Delete Contact", delete_contact),
        '10': ("Export to JSON", export_to_json),
        '11': ("Import from JSON", import_from_json),
        '12': ("Import from CSV", import_from_csv),
    }

    while True:
        print("\n--- Main Menu ---")
        for key, (description, _) in menu.items():
            print(f"  {key:>2}. {description}")
        print("   0. Exit")

        choice = input("\nSelection: ").strip()

        if choice == '0':
            print("Goodbye!")
            break
        elif choice in menu:
            try:
                menu[choice][1]()
            except Exception as e:
                print(f"Unexpected error: {e}")
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()