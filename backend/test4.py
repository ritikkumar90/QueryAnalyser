def query_check(query):
    return query.strip().rstrip(";").strip()

if __name__ == "__main__":
    query = "SELECT * FROM users;"
    sql = (query_check(query))
    print(type(sql))