
from flask import Flask, render_template, jsonify, Response, json
from flaskrss.dbconnect import Database

app = Flask(__name__)
dbConnection = Database()
connection = dbConnection.get_db_con()



@app.route('/news')
def get_trending_news():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sports LIMIT 50")
    res = cursor.fetchall()
    res_dicts=[]

    for row in res:
        print (row['key'])



    #return jsonify(res)

    return render_template('sports.html', result=res, content_type='application/json')




if __name__ == '__main__':
    app.run()

