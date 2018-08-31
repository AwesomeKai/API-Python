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
    print('Connected!')

except Exception as e:
    print e


add_rate = ("INSERT INTO forex "
               "(ID, ShortA, ShortB, CountryA, CountryB, CheckDate, Rate, Monthly, Yearly)"
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")

update_rate = ("UPDATE forex SET Rate = %s, CheckDate = %s  WHERE ID = %s")




url = 'https://ratesapi.io/api/latest?base=USD'
response = requests.get(url)

now = datetime.datetime.now()

strnow = str(now.isoformat())
print 'Updating rates at ', strnow

if response.status_code ==200:
    print 'Successfully retrieved rates!!'
    data = json.loads(response.text, use_decimal=True).get('rates', {})

    for key in data.keys():
      print 'Processing rate for : ', key

      data_rate = (str('USD') + str(key), 'USD', str(key), 'United States', 'not set', strnow, str(data[key]),0,0)

      try:
          result = dbhandler.execute(add_rate, data_rate)
          print 'Insert successful'

      except Exception as e:
          print 'Existing rate, attempting to update rate for :', key
          update_data_rate = (str(data[key]),strnow, str('USD') + str(key))
          result = dbhandler.execute(update_rate, update_data_rate)
          print 'Update successful'

      print 'Complete'

      connection.commit()



connection.close()
