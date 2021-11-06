from SchinkenDB import SchinkenClient

db_client = SchinkenClient("https://localhost", "admin", "admin")

if __name__ == '__main__':
    try:
        print(db_client.get("test"))
    except KeyError as ke:
        print(ke)
    print(db_client.set("ayo", "allo"*30000))

    print(db_client.set("pretty_long_name_bruh_but_why_not_lol_rofl_lmao_sheesh_", "not as long text"))
    print(db_client.get("pretty_long_name_bruh_but_why_not_lol_rofl_lmao_sheesh_"))

    print(db_client.get("__metadata"))
