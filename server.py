from flask import Flask, render_template, jsonify, request, session
import json, requests, hashlib, datetime

app = Flask(__name__, template_folder="pages")
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=8)
app.secret_key = hashlib.md5(b"hikey").hexdigest()

@app.before_request
def check_session():
    if "bet" not in session: session["bet"] = 0

@app.route("/")
def index():
    return render_template("atm.html")

@app.route("/api/card")
def res_card():
    #write_data()
    with open("data.json", "r") as fp:
        return jsonify(json.load(fp))

@app.route("/api/transaction", methods=["GET", "POST"])
def transaction():
    if not request.json: return jsonify(msg="沒有東西")
    type = request.json.get("type")
    amount = request.json.get("amount")
    target = request.json.get("intent")
    data = None
    with open("data.json", "r") as fp:
        data = json.load(fp)
        fp.close()
    if type == "withdraw":
        if not target or target == "": redirectURL = "https://wbank-atm.wtechhk.com"
        if target == "banker": 
            session["bet"] += int(amount)
            redirectURL = "https://wbank-atm.wtechhk.com/play/banker"
        url = f"https://wtechhk.com/wbank/auth/v1?url=/wbank/card/page/wbank/{amount}?url={redirectURL}"
        return redirect(url)
    elif type == "deposit":
        data["password"] = data["loginPw"]
        data["cardNumber"] = hashlib.sha256(f"{data['accnumber']}->{data['password']}".encode("utf-8")).hexdigest()
        resp = requests.get(url="https://wtechhk.com/wbank/hash/transfer", headers={"user":"wbank", "reviewer":data["loginUser"], "amount": str(amount)})
        if resp.status_code != 200: return jsonify(msg="Error")
        res = requests.get(url="https://wtechhk.com/wbank/card/action", headers={"cardNumber": data["cardNumber"], "password": data["password"]})
        if resp.status_code != 200: return jsonify(msg=str(res.content.decode("utf-8")))
        #write_data()
        return jsonify(balance=res.json()["balance"])
    return jsonify(msg="請求方式不支援", code=400)

@app.route("/make/money")
def make_money_page():
    #write_data()
    with open("data.json", "r") as fp:
        data = json.load(fp)
        user = data["loginUser"]
        return render_template("money.html", user=user)

@app.route("/play/<gamename>")
def play_game(gamename):
    if gamename is None: return render_template("banker.html")
    elif gamename == '': return render_template("banker.html")
    elif gamename == 'banker': return render_template("banker.html")
    elif gamename == 'majiang': return render_template("majiang.html")
    else: return render_template("banker.html")

@app.route("/wnet")
def wnet_web():
    return render_template("wnet.html")

app.run(host="0.0.0.0")