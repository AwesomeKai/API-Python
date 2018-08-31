import MySQLdb as db

HOST = "localhost"
PORT = 3306
USER = "kai_api"
PASSWORD = ""
DB = "finance"


try:
    connection = db.Connection(host=HOST, port=PORT, user=USER, passwd=PASSWORD, db=DB)
    dbhandler = connection.cursor()
    print('Connected!')
    dbhandler.execute("SELECT * from forex")
    result = dbhandler.fetchall()
    for item in result:
        print item

except Exception as e:
    print e


connection.close()
