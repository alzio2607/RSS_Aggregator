
from flask import Flask, render_template
from flaskrss import Database
from io import BytesIO
from PIL import Image
import base64


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
        top_key = cluster[0]
        query = "SELECT title,summary FROM sports where id='" + top_key + "'"
        cursor.execute(query)
        result=cursor.fetchall()
        for row in result:
            row['thumbnail'] = str(thumb_list[thumb_count])
            thumb_count+=1



        links =[]
        logos=[]
        for key in cluster:
            query = "SELECT link,publisher FROM sports where id='" + key + "'"
            cursor.execute(query)
            result1 = cursor.fetchall()
            for row in result1:
                links.append(row['link'])
                publisher = row['publisher']
                pub_blob = get_publisher_blob(publisher)
                logos.append(get_image(pub_blob))

        for row in result:
            row['links']= links
            row['logos'] = logos

        if check:
            check =0


        final_json_list.append(result[0])


    #return jsonify(final_json_list)



    #result = get_result_list(res)
    return render_template('index.html', result=final_json_list, content_type='application/json')



@app.route("/script.js")
def script():
    return render_template('script.js',result = final_json_list)

if __name__ == '__main__':
    app.run()



