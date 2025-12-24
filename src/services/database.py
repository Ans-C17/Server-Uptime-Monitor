import datetime

def create_connection(connection):
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            status TEXT NOT NULL,
            latency REAL,
            timestamp TEXT NOT NULL
        )
    """)

    connection.commit()

def insert_value(connection, url, status, latency, timestamp):
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO history (url, status, latency, timestamp) VALUES (?, ?, ?, ?)", (url, status, latency, timestamp)
    )
    
    connection.commit()

def get_previous_values(connection):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT url, status, MAX(timestamp)
        FROM history
        GROUP BY url
    """)

    rows = cursor.fetchall()
    return {row[0]: (row[1] != "WORKING", datetime.datetime.fromisoformat(row[2])) for row in rows}