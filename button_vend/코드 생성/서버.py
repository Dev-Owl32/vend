import sqlite3, random
from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)

ips = []

@app.route("/licensegen", methods=["POST"])
def Dgen():
    if request.environ.get('HTTP_X_REAL_IP', request.remote_addr) in ips:
        code = str(random.randint(1111,9999)) + '-' + str(random.randint(1111,9999)) + '-' + str(random.randint(1111,9999)) + '-' + str(random.randint(111111,999999))
        obj = request.get_json()
        con = sqlite3.connect("../DB/" + "license.db")
        cur = con.cursor()
        cur.execute("INSERT INTO license Values(?, ?, ?, ?, ?);", (code, int(obj.get('license_length')), 0, "None", 0))
        con.commit()
        con.close()
        return {'code': code}
    else:
        return {'code': '등록되지 않은 아이피'}
        
app.run("0.0.0.0", port=5050)