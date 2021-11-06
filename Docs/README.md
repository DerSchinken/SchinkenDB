# SchinkenDB 'Docs'

### SchinkenHost
```python
from SchinkenDB import SchinkenHost

host = SchinkenHost("ExampleDB")
# you can set the host and port
# example: SchinkenHost('DB_NAME', host='HOST', port=666)
# defaults are: host="localhost", port=7070

# Start the DB
host.run()
```

### SchinkenClient
```python
from SchinkenDB import SchinkenClient

db = SchinkenClient("http://localhost/", "admin", "admin")
# you can set port
# you cant change the user and password cuz why not

print(db.set("testkey", "testvalue"))
# set(key, value)
print(db.get("testkey"))
# get(key)
```
