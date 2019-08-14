from rssa.dal import MySql
from rssa.content.Fetcher import fetch
def update():
    sql = MySql()
    content = fetch()
    print('Fetch Complete')
    for key,value in content.items():
        sql.write(value, key)