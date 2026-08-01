import sqlite3

# Connect to the database
conn = sqlite3.connect('gp_notes.db')
cursor = conn.cursor()

# Check if column exists
cursor.execute("PRAGMA table_info(categories)")
columns = [row[1] for row in cursor.fetchall()]

if 'template_count' not in columns:
    cursor.execute("ALTER TABLE categories ADD COLUMN template_count INTEGER DEFAULT 0")
    conn.commit()
    print('✅ Added template_count column to categories table')
else:
    print('✅ template_count column already exists')

conn.close()