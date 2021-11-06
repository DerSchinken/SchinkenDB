from werkzeug.security import generate_password_hash, check_password_hash
from typing import Union, Any, List, Dict, Type
from paste.translogger import TransLogger
from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from BetterString import BetterString
from zlib import compress, decompress
from requests import Session
from waitress import serve

JSON = Union[Dict[str, Any], List[Any], int, str, float, bool, Type[None]]


class SchinkenHost(object):
    """
    DataBase just so i have made one this is not actually useful or fast
    and the code is no gud
    don't use under any circumstances!

    default and only user: admin
    default and only password: admin
    """
    version = "1.0.0"

    def __init__(self, database_name, host: str = "0.0.0.0", port: int = 7070) -> None:
        self.data = {}
        self.server = None

        self.__host = host
        self.__port = port

        try:
            self._load(database_name)
        except FileNotFoundError:
            self._create_db(database_name)

        self.__app = Flask("SchinkenDB")
        self.__auth = HTTPBasicAuth()

        @self.__auth.verify_password
        def verify_password(username, password):
            users = self.data["__users"]
            if username in users and check_password_hash(users.get(username), password):
                return username

        # Register routes
        @self.__app.route("/get", methods=["GET"])
        @self.__auth.login_required
        def _get():
            if not request.args.get("key"):
                return {"error": "Key not given"}

            return self.get(request.args.get("key"))

        @self.__app.route("/set", methods=["GET"])
        @self.__auth.login_required
        def _set():
            if not request.args.get("key"):
                return {"error": "Key not given"}
            if not request.args.get("value"):
                return {"error": "Value not given"}

            return self.set(request.args.get("key"), request.args.get("value"))

    def _create_db(self, name: str, suffix: str = ".sdb", user: str = "admin", _pass: str = "admin") -> None:
        """
        Create a new database
        """
        if not name.endswith(suffix):
            name += suffix

        self.data = {
            "__metadata": {
                "name": name,
                "version": self.version,
                "host": self.__host,
                "port": self.__port,
            },
            "__users": {user: generate_password_hash(_pass)},
        }
        with open(name, "wb") as f:
            f.write(compress(str(self.data).encode()))

    def _save(self) -> None:
        """
        Save the database to a file
        """
        with open(self.data["__metadata"]["name"], "wb") as f:
            f.write(compress(str(self.data).encode()))

    def _load(self, filename: str) -> None:
        """
        Load the database from a file
        """
        with open(filename, 'rb') as f:
            self.data = eval(decompress(f.read()).decode())

    def run(self, app_secret: str = None, url_scheme: str = None) -> None:
        """
        Run the server
        """
        self.__app.secret_key = app_secret
        print(f"Starting server on {self.__host}:{self.__port}/".replace("0.0.0.0", "localhost"))
        serve(TransLogger(self.__app), host=self.__host, port=self.__port, url_scheme=url_scheme)
        # self.__app.run(host=self.__host, port=self.__port, debug=self.__debug)

    def get(self, key: str) -> JSON:
        """
        Get a value from the database
        """
        if key == "users":
            return jsonify({"error": "Key 'users' not found"})
        try:
            return jsonify(self.data[key])
        except KeyError:
            return jsonify({"error": f"Key '{key}' not found"})

    def set(self, key: str, value) -> JSON:
        """
        Set a value in the database
        """
        if key == "__metadata":
            return jsonify({"error": "Cannot set '__metadata'"})
        if key == "users":
            return jsonify({"error": "Cannot set 'users'"})

        self.data[key] = value
        self._save()
        return jsonify({"success": f"Key '{key}' set"})

    def __repr__(self) -> str:
        return f"Hosting '{self.data['__metadata']['name']}' on version '{self.version}'"


class SchinkenClient(object):
    """
    SchinkenClient is a simple client for SchinkenHost
    """
    version = "1.0.0"

    def __init__(self, host: str, user: str, password: str, port: int = 7070) -> None:
        self.host = host
        self.port = port
        self.user = user
        self.password = password

        self.url = f"{host}:{str(port)}"

        # Try to connect to the server
        self.con = Session()
        self.con.auth = (user, password)
        self.con.headers.update({
            "User-Agent": f"SchinkenClient v{self.version}",
        })

        self.host_data = self.con.get(f"{self.url}/get?key=__metadata", timeout=10)

        self.host_data.raise_for_status()
        self.host_data = self.host_data.json()

        # Check mayor version
        if not self.version[0] == self.host_data.get("version")[0]:
            raise ValueError(f"Version mismatch! Client: {self.version}; Server: {self.host_data.get('version')}")
        # check minor versions
        if not self.version[:-2] == self.host_data.get("version")[:-2]:
            print(f"Warning: Version of client and server don't match! \
            Client: {self.version}; Server: {self.host_data.get('version')}".replace("    ", ""))
        # check patch version maybe later or not

    def get(self, key) -> any:
        """
        Gets value from db
        if value is a str it will be converted to a BetterString
        """
        resp = self.con.get(f"{self.url}/get?key={key}")
        resp.raise_for_status()
        if not isinstance(resp.json(), str) and resp.json().get("error"):
            raise KeyError(resp.json().get("error"))

        if isinstance(resp.json(), str):
            return BetterString(resp.json())
        return resp.json()

    def set(self, key, value) -> str:
        """
        Sets key to value in db
        """
        resp = self.con.get(f"{self.url}/set?key={key}&value={value}")
        resp.raise_for_status()

        if resp.json().get("error"):
            raise KeyError(resp.json().get("error"))

        return resp.json()["success"]
