
from flask import Flask, render_template,json,jsonify
from flaskrss import Database
from io import BytesIO
from PIL import Image
import base64
from datetime import datetime



app = Flask(__name__)
dbConnection = Database()
connection = dbConnection.get_db_con()

result=[]
category=None
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


def get_result(category):
    final_json_list = []
    cursor = connection.cursor()
    query = "SELECT ids,thumbnail FROM clusters WHERE category ='"+category+"' and ts = (select max(ts) from clusters) ORDER BY publisher_count DESC ,publish_ts DESC LIMIT 50"
    cursor.execute(query)
    res = cursor.fetchall()
    ids_list = []
    thumb_list = []
    for row in res:
        list = row['ids'].split(',')[:6]
        ids_list.append(list)
        thumb_list.append(get_image(row['thumbnail']))
    thumb_count = 0
    for cluster in ids_list:
        cluster_dict = {}
        cluster_dict['thumbnail'] = str(thumb_list[thumb_count])
        cluster_dict['article_list'] = []
        thumb_count += 1
        for key in cluster:
            query = "SELECT title,link,publisher,publish_ts FROM "+category+ " where id='" + key + "'"
            cursor.execute(query)
            result = cursor.fetchall()
            for row in result:
                ts = row['publish_ts']
                if not ts:
                    row['publish_ts']=""
                    break
                dt = datetime.strptime(ts, '%Y%m%d%H%M')
                delta = datetime.now() - dt
                days, seconds = delta.days, delta.seconds
                if days:
                    if days == 1:
                        row['publish_ts'] = str(days) + " day ago"
                    elif days > 1:
                        row['publish_ts'] = str(days) + " days ago"
                else:
                    hours = seconds // 3600
                    minutes = (seconds % 3600) // 60
                    if hours:
                        row['publish_ts'] = str(hours) + " hours ago"
                    else:
                        row['publish_ts'] = str(minutes) + " minutes ago"
            for k,v in result[0].items():
                if v is None:
                    result[0][k] = "null"
            cluster_dict['article_list'].append(result[0])
        for k,v in cluster_dict.items():
            if v is None:
                cluster_dict[k] = "null"
        final_json_list.append(cluster_dict)
    return final_json_list



@app.route('/sports')
def sports():
    global result,category
    result = get_result("sports")
    category='sports'
    return render_template('index.html',category='sports',content_type='application/json')


@app.route('/business')
def business():
    global result,category
    category='business'
    result = get_result("business")
    return render_template('index.html',category='business',content_type='application/json')


@app.route('/technology')
def technology():
    global result,category
    result = get_result("technology")
    category='technology'
    return render_template('index.html',category='technology',content_type='application/json')



@app.route('/health')
def health():
    global result,category
    category='health'
    result = get_result("health")
    return render_template('index.html',category='health',content_type='application/json')


@app.route('/science')
def science():
    global result,category
    category='science'
    result = get_result("science")
    return render_template('index.html',category='science',content_type='application/json')\


@app.route('/world')
def world():
    global result,category
    category='world'
    result = get_result("world")
    return render_template('index.html',content_type='application/json')

@app.route('/home')
def home():
    global result,category
    category='trending'
    result = get_result("trending")
    print('result received')
    print(len(result))
    return render_template('index.html',content_type='application/json')

@app.route('/')
def trending():
    global result,category
    category='trending'
    result = get_result("trending")
    return render_template('index.html',content_type='application/json')

@app.route('/entertainment')
def entertainment():
    global result,category
    category='entertainment'
    result = get_result("entertainment")
    return render_template('index.html',content_type='application/json')



@app.route("/script.js")
def script():
    global result,category
    print(category)
    print('result size : {}'.format(len(result)))
    print('sample result : ')
    print(result[0]['thumbnail'])
    print(result[0]['article_list'][0])

    return render_template('script.js',result=result,category=category)

if __name__ == '__main__':
    app.run(debug=True)