"""Main script for the Password Manager"""
import argparse
import logging
import sqlite3 as sql

from connector import Connector
from credential import Credential


logger = logging.getLogger("passman")


def parse_args():
    parser = argparse.ArgumentParser(description="Password Manager",
                                     allow_abbrev=False)
    parser.add_argument('-v', "--verbose", action="store_true",
                        help="print info logs to the console")

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('--database', help="database (.db) file to store/fetch password from")

    subparser = parser.add_subparsers(title='Commands', dest="action")

    store_parser = subparser.add_parser('store', parents=[parent_parser],
                                        help="store password")
    store_parser.add_argument('--url', help="url for the service")
    store_parser.add_argument('--userid', metavar='USERNAME | EMAIL | MOBILE',
                              help='userid for the service')
    store_parser.add_argument('service', metavar='SERVICE',
                              help="name of the service to store password")
    store_parser.add_argument('passwd', metavar='PASSWORD',
                              help="password for the service")

    fetch_parser = subparser.add_parser('fetch', parents=[parent_parser],
                                        help="fetch password")
    fetch_parser.add_argument('service', metavar='SERVICE',
                              help="service name of the password to fetch")
    
    list_parser = subparser.add_parser('list', parents=[parent_parser], 
                                       help='list services')
    
    return parser.parse_args()


def main():
    args = parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    
    logger.info("Starting script with arguments: %s", args)

    conn = sql.connect(args.database)
    curs = conn.cursor()

    if args.action == 'store':
        # Store password to the database
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
    elif args.action == 'fetch':
        curs.execute("SELECT userid, passwd FROM credentials WHERE service = :service", {"service": args.service})
        res = curs.fetchone()
        print(f"userid: {res[0]}\npasswd: {res[1]}")
    elif args.action == 'list':
        curs.execute("SELECT service, url, userid FROM credentials")
        # TODO: Prettify output formatting
        print("service\turl\tuserid", '-'*30, sep="\n")
        for r in curs.fetchall():
            print(*r, sep="\t")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
