from .SchinkenDB import SchinkenHost
from os import urandom
import argparse

# initialising the arg parser
cli = argparse.ArgumentParser(
    description="Start a SchinkenDB vie the console",
    prog='SchinkenDB',
)

# adding the arguments
cli.add_argument("start", nargs="+", help="Start the DB")
cli.add_argument("--host", type=str, help="Host on which the DB will be running (default localhost)")
cli.add_argument("-p", "--port", type=str, help="Port on which the DB will be running (default 7070)")
cli.add_argument("-s", "--secret", type=str, help="App secret key (default random (will be printed in console))")

# getting the args
args = cli.parse_args()

try:
    db_name = str(args.start[1])
except IndexError:
    print("DB name not specified")
    exit(-1)

if args.host:
    host = str(args.host)
else:
    host = "0.0.0.0"

if args.port:
    port = int(args.port)
else:
    port = 7070

if args.secret:
    app_secret = args.secret
else:
    app_secret = urandom(32).hex()
    print(f"App secret: {app_secret}")

# noinspection PyUnboundLocalVariable
# cuz it is stupid and it will be defined there is no chance that is isn't
db = SchinkenHost(db_name, host, port)
db.run()
