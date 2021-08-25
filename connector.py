import sqlite3 as sql


# Ideally the database should be passed from the main script (passman.py)
DATABASE = "data/example.db"
# DATABASE = ":memory:"


class Connector:
    """Class for connecting to database"""
    def __init__(self, database):
        self.connection = sql.connect(database)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.commit()
        self.cursor.close()


def select_data(cur, target="*", cond=None):
    return cur.execute("SELECT * FROM credentials")


def insert_data(cur):
    cur.execute("""INSERT INTO credentials
                 VALUES ('Facebook', NULL, 'johndoe', 'p@55w0rd', 'fb')""")
    cur.execute("INSERT INTO credentials VALUES (?, ?, ?, ?, ?)",
                ('Twitter', 'https://twitter.com', 'johndoe', 'incorrect', None))
    cur.execute("INSERT INTO credentials VALUES (?, ?, ?, ?, ?)",
                ("Amazon", None, "johndoe@email.com", "pass1234", "amz"))


def create_table(cur):
    cur.execute("""CREATE TABLE credentials (
                service text,
                url text,
                userid text,
                passwd text,
                alias text
                )""")


def main():
    con = sql.connect(DATABASE)
    cur = con.cursor()

    # create_table(cur)
    # insert_data(cur)

    result = select_data(cur)

    con.commit()    # not necessary when using :memory:
    for r in result:
        print(r)
    con.close()


if __name__ == "__main__":
    main()

