import sqlite3
import os

# Use the correct path for the database
db_path = os.path.join(os.getcwd(), 'artisans.db')
# For Render deployment, the app is in /app, so uncomment the line below if needed
# db_path = '/app/artisans.db'

conn = sqlite3.connect(db_path)
c = conn.cursor()

# Add materials column to artisans table if not exists
try:
    c.execute("ALTER TABLE artisans ADD COLUMN materials TEXT")
except sqlite3.OperationalError:
    # Column already exists
    pass

# Add approval_status and include_quote columns to generated_content table
try:
    c.execute("ALTER TABLE generated_content ADD COLUMN approval_status TEXT DEFAULT 'pending'")
except sqlite3.OperationalError:
    pass

try:
    c.execute("ALTER TABLE generated_content ADD COLUMN include_quote INTEGER DEFAULT 1")
except sqlite3.OperationalError:
    pass

conn.commit()
conn.close()
print("Database schema updated with materials, approval_status, and include_quote columns.")
