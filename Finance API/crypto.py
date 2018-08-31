from decimal import Decimal
import simplejson as json
import requests
import datetime
import MySQLdb as db

HOST = "localhost"
PORT = 3306
USER = "kai_api"
PASSWORD = ""
DB = "finance"

try:
    connection = db.Connection(host=HOST, port=PORT, user=USER, passwd=PASSWORD, db=DB)
    dbhandler = connection.cursor()
    print('DB Connected!')

except Exception as e:
    print e


add_crypto = ("INSERT INTO crypto "
               "(ID, Description, Price, CheckDate, Volume)"
               "VALUES (%s, %s, %s, %s, %s)")

#update_crypto = ("UPDATE forex SET Rate = %s, CheckDate = %s  WHERE ID = %s")




url = 'https://api.coinmarketcap.com/v2/ticker/'
response = requests.get(url)

now = datetime.datetime.now()

strnow = str(now.isoformat())
print 'Updating rates at ', strnow

if response.status_code ==200:
    print 'Successfully retrieved crypto price!!'
    data = json.loads(response.text, use_decimal=True).get('data', {})

    for key in data.keys():
      print 'Processing crypto for : ', data[key]['name']

      data_rate = (str(data[key]['symbol']),str(data[key]['name']), data[key]['quotes']['USD']['price'], strnow, data[key]['quotes']['USD']['volume_24h'])

      try:
          result = dbhandler.execute(add_crypto, data_rate)
          print 'Insert successful'

      except Exception as e:
          print e



      connection.commit()

else :
    print 'API Data Retrival failed! '

print 'Complete'

connection.close()
