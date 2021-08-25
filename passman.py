"""Main script for the Password Manager"""
import argparse
import sqlite3 as sql

from connector import Connector
from credential import Credential


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '-db', '--database',
                        help="path to database (.db) file")
    parser.add_argument('--put',
                        action="store_true",
                        help="add credential to database")
    parser.add_argument('--get',
                        action="store_true",
                        help="retrieve credential from database")
    parser.add_argument('--service',
                        help="name of the service")
    return parser.parse_args()


def main():
    args = parse_args()

    conn = sql.connect(args.database)
    curs = conn.cursor()

    if args.put:
        pass

    if args.get:
        curs.execute("SELECT userid, passwd FROM credentials WHERE service = :service", {"service": args.service})
        res = curs.fetchone()
        print(f"userid: {res[0]}\npasswd: {res[1]}")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()

