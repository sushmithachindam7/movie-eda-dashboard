import streamlit as st
import sqlite3

# --- Database Setup ---
conn = sqlite3.connect("contacts.db")
c = conn.cursor()

# Create table if not exists
c.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        message TEXT
    )
''')
conn.commit()

# --- Streamlit Contact Form ---
st.title("📬 Contact Form")

with st.form("contact_form"):
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_area("Your Message")
    submitted = st.form_submit_button("Submit")

    if submitted:
        if name and email and message:
            c.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",
                      (name, email, message))
            conn.commit()
            st.success("✅ Your message has been saved to the database!")
        else:
            st.error("⚠️ Please fill in all fields.")
