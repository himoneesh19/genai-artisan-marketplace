import sqlite3

conn = sqlite3.connect('artisans.db')
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
