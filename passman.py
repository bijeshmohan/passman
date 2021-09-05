#!/bin/python3
"""Main script for the Password Manager"""
import argparse
import logging
import sqlite3 as sql
import sys


logger = logging.getLogger("passman")


def tabulate(data, title=None):
    """Tabularize data for representation"""
    widths = [max(map(lambda x: len(x) if x else 0, col)) for col in zip(*data)]

    rows = []
    if title:
        title_row = (" " * 4).join([t.ljust(widths[i]) for i, t in enumerate(title)])
        rows.append(title_row)
        rows.append("-" * len(title_row))
    for row in data:
        cells = [e.ljust(widths[i]) if e else " " * widths[i] for i, e in enumerate(row)]
        rows.append((" " * 4).join(cells))

    return "\n".join(rows)


def parse_args():
    """Parse command-line arguments for the program"""
    parser = argparse.ArgumentParser(description="Password Manager", allow_abbrev=False)
    parser.add_argument('-v',
                        '--verbose',
                        action="store_true",
                        help="increase the verbosity of the program")

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument("--database",
                               metavar="DATABASE",
                               required=True,
                               help="database (.db) file containing passwords")

    subparser = parser.add_subparsers(title="Commands", dest="action")
    store_parser = subparser.add_parser("store",
                                        parents=[parent_parser],
                                        help="store password")
    fetch_parser = subparser.add_parser("fetch",
                                        parents=[parent_parser],
                                        help="fetch password")
    list_parser = subparser.add_parser("list",
                                       parents=[parent_parser],
                                       help="list services")

    store_parser.add_argument("--url",
                              help="url for the service")
    store_parser.add_argument("--userid",
                              metavar="USERNAME | EMAIL | MOBILE",
                              help="userid for the service")
    store_parser.add_argument("service",
                              metavar="SERVICE",
                              help="name of the service to store password")
    store_parser.add_argument("passwd",
                              metavar="PASSWORD",
                              help="password for the service")

    fetch_parser.add_argument("service",
                              metavar="SERVICE",
                              help="service name of the password to fetch")
    
    list_parser.add_argument('--url',
                             action='store_true',
                             help='list associated url')
    list_parser.add_argument('--userid',
                             action='store_true',
                             help='list associated userid')

    args = parser.parse_args()
    if not args.action:
        parser.print_usage()
        sys.exit()
    return args


def main():
    args = parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
        logger.info("Starting script with arguments: %s", args)

    conn = sql.connect(args.database)
    curs = conn.cursor()

    if args.action == "store":
        try:
            curs.execute(
                "INSERT INTO credentials VALUES (?, ?, ?, ?)",
                (args.service, args.url, args.userid, args.passwd),
            )
        except sql.OperationalError:
            logger.warning(
                """Table 'credentials' NOT found!
                Creating table 'credentials'..."""
            )
            curs.execute(
                """CREATE TABLE credentials (
                service text,
                url text,
                userid text,
                passwd text
                )"""
            )
            curs.execute(
                "INSERT INTO credentials VALUES (?, ?, ?, ?)",
                (args.service, args.url, args.userid, args.passwd)
            )
    elif args.action == "fetch":
        curs.execute(
            "SELECT userid, passwd FROM credentials WHERE service = :service",
            {"service": args.service},
        )
        res = curs.fetchone()
        print(f"userid: {res[0]}\npasswd: {res[1]}")
    elif args.action == "list":
        cols = ["service", "url"]
        curs.execute(f"SELECT {', '.join(cols)} FROM credentials")
        res = curs.fetchall()
        output = tabulate(res, title=cols)
        print(output)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
