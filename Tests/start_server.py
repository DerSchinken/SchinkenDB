from SchinkenDB import SchinkenHost

db_host = SchinkenHost("test_db.sdb")

if __name__ == '__main__':
    db_host.run(url_scheme="https")
