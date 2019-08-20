import sqlalchemy as sql

"""#SQL_USERNAME = "skenzo_dev"
SQL_USERNAME = "root"
SQL_PASSWORD = "Skenzo_Dev"
SQL_HOSTNAME = "localhost"
SQL_DBNAME = "Rss"
connection = sql.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                               format(SQL_USERNAME, SQL_PASSWORD,
                                      SQL_HOSTNAME, SQL_DBNAME))
"""
import pandas as pd
import matplotlib.pyplot as plt

from io import BytesIO
from PIL import Image


df = pd.read_csv("publishers.csv")

df['score']=0
print(df)
def get_blob(url):
    img = Image.open(open(url, 'rb'))
    img = img.resize((300, 300))
    stream = BytesIO()
    img.save(stream, format="PNG")
    return img, stream.getvalue()


logos = []


print (get_blob("/Users/ayush.goya/Downloads/logos/nyt.png")[0])



logos.append(get_blob("/Users/ayush.goya/Downloads/logos/nyt.png")[1])
logos.append(get_blob("/Users/ayush.goya/Downloads/logos/bbc.png")[1])
logos.append(get_blob("/Users/ayush.goya/Downloads/logos/buzzfeed.jpg")[1])
logos.append(get_blob("/Users/ayush.goya/Downloads/logos/cnn.png")[1])
logos.append(get_blob("/Users/ayush.goya/Downloads/logos/guardian.png")[1])
logos.append(get_blob("/Users/ayush.goya/Downloads/logos/reuters.png")[1])
logos.append(get_blob("/Users/ayush.goya/Downloads/logos/wp.png")[1])
logos.append(get_blob("/Users/ayush.goya/Downloads/logos/toi.png")[1])
logos.append(get_blob("/Users/ayush.goya/Downloads/logos/ndtv.jpg")[1])
logos.append(get_blob("/Users/ayush.goya/Downloads/logos/independent.png")[1])
logos.append(get_blob("/Users/ayush.goya/Downloads/logos/daily.png")[1])
logos.append(get_blob("/Users/ayush.goya/Downloads/logos/cnbc.png")[1])
logos.append(get_blob("/Users/ayush.goya/Downloads/logos/mirror.jpg")[1])
logos.append(get_blob("/Users/ayush.goya/Downloads/logos/time.png")[1])
logos.append(get_blob("/Users/ayush.goya/Downloads/logos/cbs.jpg")[1])
logos.append(get_blob("/Users/ayush.goya/Downloads/logos/sun.jpg")[1])

df['logo'] = logos
#df.to_pickle('./logos.pkl')
print(df['logo'][0])
print(df['logo'][1])

