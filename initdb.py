import sqlite3

connect = sqlite3.connect("database.db")
c = connect.cursor()

c.execute("""

    DROP TABLE IF EXISTS logins

""")

c.execute("""

    CREATE TABLE logins (
        username TEXT PRIMARY KEY NOT NULL,
        password TEXT NOT NULL,'
    )


""")

connect.commit()
connect.close()