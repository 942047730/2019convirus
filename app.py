import string

from flask import Flask, request, jsonify
from flask import render_template
import json

from jieba.analyse import extract_tags

import utils
import decimal

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("main.html")


@app.route('/tem')
def hello_world1():
    return render_template("index.html")


@app.route('/ajax', methods=["get", "post"])
def hello_world2():
    name = request.values.get("name")
    score = request.values.get("score")
    print(f"name:{name},score:{score}")
    return '10000'


@app.route('/time')
def get_time():
    return utils.get_time()


@app.route("/c1")
def get_c1_data():
    data = utils.get_c1_data()
    # print(str(data[0]))
    # print("'"+ data[0]+"'")
    # d = json.dumps({"confirm":"'"+ str(data[0])+"'", "suspect": "'"+ str(data[1])+"'", "heal":"'"+ str(data[2])+"'", "dead":"'"+ str(data[3])+"'"})
    # print(d)
    # return d
    d1 = int(data[0])
    d2 = int(data[1])
    d3 = int(data[2])
    d4 = int(data[3])
    return jsonify({"confirm": d1, "suspect": d2, "heal": d3, "dead": d4})


@app.route("/c2")
def get_c2_data():
    res = []
    print()
    for tup in utils.get_c2_data():
        res.append({"name": tup[0], "value": int(tup[1])})
    return jsonify({"data": res})


@app.route("/l1")
def get_l1_data():
    data = utils.get_l1_data()
    day, confirm, suspect, heal, dead = [], [], [], [], []
    sumB=0
    sumC=0
    sumD=0
    sumE=0
    for a, b, c, d, e in data[7:]:
        sumB = b + sumB
        sumC = c + sumC
        sumD = d + sumD
        sumE = e + sumE
        day.append(a.strftime("%m-%d"))  # a是datatime类型
        confirm.append(sumB)
        suspect.append(sumC)
        heal.append(sumD)
        dead.append(sumE)
    return jsonify({"day": day, "confirm": confirm, "suspect": suspect, "heal": heal, "dead": dead})


@app.route("/l2")
def get_l2_data():
    data = utils.get_l2_data()
    day, confirm, suspect = [], [], []
    for a, b, c in data[7:]:
        day.append(a.strftime("%m-%d"))  # a是datatime类型
        confirm.append(b)
        suspect.append(c)
    return jsonify({"day": day, "confirm": confirm, "suspect": suspect})

@app.route("/r1")
def get_r1_data():
    data = utils.get_r1_data()
    city = []
    confirm = []
    for k,v in data:
        city.append(k)
        confirm.append(int(v))
    return jsonify({"city": city, "confirm": confirm})

@app.route("/r2")
def get_r2_data():
    data = utils.get_r2_data() #格式 (('民警抗疫一线奋战16天牺牲1037364',), ('四川再派两批医疗队1537382',)
    d = []
    for i in data:
        k = i[0].rstrip(string.digits)  # 移除热搜数字
        v = i[0][len(k):]  # 获取热搜数字
        ks = extract_tags(k)  # 使用jieba 提取关键字
        for j in ks:
            if not j.isdigit():
                d.append({"name": j, "value": v})
    return jsonify({"kws": d})

if __name__ == '__main__':
    app.run()
