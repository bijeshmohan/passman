"""Main script for the Password Manager"""
import argparse
import logging
import sqlite3 as sql

from connector import Connector
from credential import Credential


logger = logging.getLogger("passman")


def parse_args():
    parser = argparse.ArgumentParser(description="Password Manager", allow_abbrev=False)
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help="show logs to the console")
    parser.add_argument('-d', '-db', '--database',
                        help="path to database (.db) file")
    parser.add_argument('--store',
                        action="store_true",
                        help="add credential to database")
    parser.add_argument('--fetch',
                        action="store_true",
                        help="retrieve credential from database")
    parser.add_argument('--list',
                        action="store_true",
                        help="lists the services (with other attributes) stored in the database")
    parser.add_argument('--service',
                        help="name of the service",
                        required=True)
    parser.add_argument('--url',
                        help="url for the service")
    parser.add_argument('--userid',
                        help="userid for the service")
    parser.add_argument('--passwd',
                        help="password for the service")
    
    args = parser.parse_args()
    # TODO: Implement conditions
    return args


def main():
    args = parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    
    logger.info("Starting script with arguments: %s", args)

    conn = sql.connect(args.database)
    curs = conn.cursor()

    if args.store:
        try:
            curs.execute("INSERT INTO credentials VALUES (?, ?, ?, ?)",
                         (args.service, args.url, args.userid, args.passwd))
        except sql.OperationalError:
            logger.warning("Table 'credentials' NOT found! Creating the table for storing credentials...")
            curs.execute("""CREATE TABLE credentials (
                         service text,
                         url text,
                         userid text,
                         passwd text
                         )""")
            curs.execute("INSERT INTO credentials VALUES (?, ?, ?, ?)",
                         (args.service, args.url, args.userid, args.passwd))

    if args.fetch:
        curs.execute("SELECT userid, passwd FROM credentials WHERE service = :service", {"service": args.service})
        res = curs.fetchone()
        print(f"userid: {res[0]}\npasswd: {res[1]}")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
