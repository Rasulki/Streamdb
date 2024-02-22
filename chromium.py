import sqlite3
from sqlite3 import Error
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import tkinter as tk
from tkinter import Listbox
from googletrans import Translator
import random

# Translate Message
def translate_message(message):
    translator = Translator()
    translation = translator.translate(message, dest='ru')
    return translation.text

# Insert into DB
def insert_message(conn, russian, english):
    try:
        c = conn.cursor()
        c.execute("INSERT INTO messages(string_rus, string_eng) VALUES (?, ?)", (russian, english))
        conn.commit()
    except Error as e:
        print(e)

# Initialize Headless Browser
def get_chromium_driver(conn):
    driver = webdriver.Chrome()
    driver.get("https://www.twitch.tv/loltyler1")
    time.sleep(4)

    chat_messages = []
    start_time = time.time()
    while time.time() - start_time < 20:
        elements = driver.find_elements(By.CLASS_NAME, "chat-line__message")
        for element in elements:
            if element.text not in chat_messages:
                chat_messages.append(element.text)
                text = element.text
                insert_text = text[text.find(": ")+1:].strip()
                translated_message = translate_message(insert_text)
                insert_message(conn, translated_message, insert_text)
                #print(insert_text)
        time.sleep(1) 
    driver.quit()

# Create Connection to DB
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('wordCount.db') 
        return conn
    except Error as e:
        print(e)

#Drop Table and Create New One
def create_table(conn):
    try:
        c = conn.cursor()
        #c.execute("DROP TABLE IF EXISTS messages")
        c.execute("""
            CREATE TABLE messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                string_rus TEXT NOT NULL,
                string_eng TEXT NOT NULL,
                insert_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                review INTEGER DEFAULT 1
            )
        """)
        
    except Error as e:
        print(e)


# Print Statement
def select_top_5(conn):
    try:
        c = conn.cursor()
        c.execute("SELECT max(id) max_num from messages")
        # fetchall() returns tuples
        result = c.fetchall()
        max_id = int(result[0][0])
        number = random.randint(1, max_id)
        return number
    except Error as e:
        print(e)


# --- tkinter ---
def on_button_click():
    print("Button clicked!")

def main():
    conn = create_connection()
    c = conn.cursor()
    if conn is not None:
        #create_table(conn)
        #get_chromium_driver(conn)
        result = select_top_5(conn)
        print(result)

        #--- GUI ---
        root = tk.Tk()
        #listbox = Listbox(root)
        c.execute("SELECT string_rus FROM messages WHERE id = {}".format(result))
        query = c.fetchall()
        label = tk.Label(root, text=query)
        button = tk.Button(root, text="One Day", command=on_button_click)
        #listbox.pack()
        label.pack()
        button.pack()
        #for result in results:
        #    listbox.insert(tk.END, result)
        root.mainloop()

    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()