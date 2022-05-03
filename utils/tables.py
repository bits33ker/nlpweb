import sqlite3
# https://www.geeksforgeeks.org/python-sqlite-create-table/#:~:text=Establish%20the%20connection%20or%20create,method%20of%20the%20Cursor%20class.
# https://pythonexamples.org/python-sqlite3-create-table/
# Connecting to sqlite
# connection object
connection_obj = sqlite3.connect('db.sqlite3')

# cursor object
cursor_obj = connection_obj.cursor()

# Drop the GEEK table if already exists.
cursor_obj.execute("DROP TABLE IF EXISTS Contact")

# Creating table
table = """ CREATE TABLE Contact (
			id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL
		); """

cursor_obj.execute(table)

print("Table Contact is Ready")

cursor_obj.execute("DROP TABLE IF EXISTS WhatsAppGroup")

# Creating table
table = """ CREATE TABLE WhatsAppGroup (
			id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL
		); """

cursor_obj.execute(table)

print("Table WhatsAppGroup is Ready")

cursor_obj.execute("DROP TABLE IF EXISTS WhatsApp")

table = """ CREATE TABLE WhatsApp (
			id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            contact integer NOT NULL,
            whatsappgroup integer NOT NULL,
            dt_message datetime NOT NULL,
            message VARCHAR(255) NOT NULL,
            FOREIGN KEY(contact) REFERENCES Contact(id),
            FOREIGN KEY(whatsappgroup) REFERENCES WhatsAppGroup(id)
		); """

cursor_obj.execute(table)

print("Table WhatsApp is Ready")


# Close the connection
connection_obj.close()
