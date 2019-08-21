
from flask import Flask, render_template,json,jsonify
from flaskrss import Database
from io import BytesIO
from PIL import Image
import base64
from datetime import datetime



app = Flask(__name__)
dbConnection = Database()
connection = dbConnection.get_db_con()

final_json_list = []

def get_image(blob):
    final_img=""
    if blob:
        image = Image.open(BytesIO(blob))
        output = BytesIO()
        image.save(output,'PNG',quality = 100)
        output.seek(0)
        img = base64.b64encode(output.getvalue())
        final_img = img.decode('ascii')
    return final_img

def get_publisher_blob(publisher):
    cursor = connection.cursor()
    query = "SELECT logo from publisher_data where PUBLISHER='" +str(publisher) + "'"
    cursor.execute(query)
    result = cursor.fetchall()
    pub_blob=""
    for row in result:
        pub_blob = row['logo']
    return pub_blob




@app.route('/sports')
def get_sports_news():
    global final_json_list
    check=1
    final_json_list=[]
    cursor = connection.cursor()
    cursor.execute("SELECT ids,thumbnail FROM clusters WHERE category ='sports' and ts = (select max(ts) from clusters) ORDER BY publisher_count DESC ,publish_ts DESC LIMIT 100")
    res = cursor.fetchall()
    ids_list=[]
    thumb_list=[]
    for row in res:
        list = row['ids'].split(',')[:6]
        ids_list.append(list)

        thumb_list.append(get_image(row['thumbnail']))


    thumb_count = 0
    for cluster in ids_list:
        cluster_dict = {}
        cluster_dict['thumbnail'] = str(thumb_list[thumb_count])
        cluster_dict['article_list']=[]
        thumb_count += 1
        for key in cluster:
            query = "SELECT title,link,publisher,publish_ts FROM sports where id='" + key + "'"
            cursor.execute(query)
            result=cursor.fetchall()
            for row in result:
                ts = row['publish_ts']
                dt = datetime.strptime(ts, '%Y%m%d%H%M')
                delta = datetime.now() - dt
                days,seconds = delta.days,delta.seconds
                if days:
                    if days==1:
                        row['publish_ts'] = str(days) + " day ago"
                    elif days>1:
                        row['publish_ts'] = str(days) + " days ago"
                else:
                    hours = seconds // 3600
                    minutes = (seconds % 3600) // 60
                    if hours:
                        row['publish_ts'] = str(hours) + " hours ago"
                    else:
                        row['publish_ts'] = str(minutes) + " minutes ago"

            cluster_dict['article_list'].append(result[0])

        final_json_list.append(cluster_dict)

    #return jsonify(final_json_list)
    return render_template('index.html', result=final_json_list, category='sports', content_type='application/json')



@app.route("/script.js")
def script():
    return render_template('script.js',result = final_json_list)

if __name__ == '__main__':
    app.run()



