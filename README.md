# SchinkenDB
DataBase just so I have made one this is not actually useful or fast   
and the code is no gud   
don't use under any circumstances!   

default and only user: admin   
default and only password: admin   
(at least for now)

Host:
```python
from SchinkenDB import SchinkenHost

db = SchinkenHost("FileName.sdb")
db.run()
```
Client:
```python
from SchinkenDB import SchinkenClient

db = SchinkenClient("http://localhost/", "admin", "admin")

print(db.set("t", "test"))
print(db.get("t"))
```
