import sqlite3
import os

# Use the Render database path
db_path = os.environ.get('DATABASE_URL', 'gp_notes.db')
if db_path.startswith('sqlite:///'):
    db_path = db_path.replace('sqlite:///', '')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if column exists
cursor.execute('PRAGMA table_info(categories)')
columns = [row[1] for row in cursor.fetchall()]

if 'template_count' not in columns:
    cursor.execute('ALTER TABLE categories ADD COLUMN template_count INTEGER DEFAULT 0')
    conn.commit()
    print('✅ Added template_count column to categories table')
else:
    print('✅ Column already exists')

conn.close()