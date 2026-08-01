import sqlite3
import os

def add_template_count_column():
    # Use the database file from Render's environment
    db_path = os.environ.get('DATABASE_URL', 'gp_notes.db')
    
    # Remove sqlite:/// prefix if present
    if db_path and db_path.startswith('sqlite:///'):
        db_path = db_path.replace('sqlite:///', '')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if column exists
        cursor.execute("PRAGMA table_info(categories)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'template_count' not in columns:
            cursor.execute("ALTER TABLE categories ADD COLUMN template_count INTEGER DEFAULT 0")
            conn.commit()
            print("✅ Added template_count column successfully!")
        else:
            print("✅ Column already exists!")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    add_template_count_column()