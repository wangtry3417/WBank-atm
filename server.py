from flask import Flask, render_template, jsonify, request
import json, requests, hashlib
from main import write_data

app = Flask(__name__, template_folder="pages")

@app.route("/")
def index():
    return render_template("atm.html")

@app.route("/api/card")
def res_card():
    write_data()
    with open("data.json", "r") as fp:
        return jsonify(json.load(fp))

@app.route("/api/transaction", methods=["GET", "POST"])
def transaction():
    if not request.json: return jsonify(msg="沒有東西")
    type = request.json.get("type")
    amount = request.json.get("amount")
    data = None
    with open("data.json", "r") as fp:
        data = json.load(fp)
        fp.close()
    if type == "withdraw":
        data["password"] = data["loginPw"]
        data["cardNumber"] = hashlib.sha256(f"{data['accnumber']}->{data['password']}".encode("utf-8")).hexdigest()
        data["accessKey"] = "12309"
        data["reviewer"] = "wbank"
        data["amount"] = str(amount)
        resp = requests.patch(url="https://wtechhk.com/wbank/card/action", json=data)
        if resp.status_code != 200: return jsonify(newBalance=data["balance"], message="請求失敗", error=True)
        write_data()
        return jsonify(newBalance=data["balance"], message=resp.json()["message"])
    elif type == "deposit":
        data["password"] = data["loginPw"]
        data["cardNumber"] = hashlib.sha256(f"{data['accnumber']}->{data['password']}".encode("utf-8")).hexdigest()
        resp = requests.get(url="https://wtechhk.com/wbank/hash/transfer", headers={"user":"wbank", "reviewer":data["loginUser"], "amount": str(amount)})
        if resp.status_code != 200: return jsonify(msg="Error")
        res = requests.get(url="https://wtechhk.com/wbank/card/action", headers={"cardNumber": data["cardNumber"], "password": data["password"]})
        if resp.status_code != 200: return jsonify(msg=str(res.content.decode("utf-8")))
        write_data()
        return jsonify(balance=res.json()["balance"])
    return jsonify(msg="請求方式不支援", code=400)

@app.route("/make/money")
def make_money_page():
    write_data()
    with open("data.json", "r") as fp:
        data = json.load(fp)
        user = data["loginUser"]
        return render_template("money.html", user=user)

app.run(host="0.0.0.0")