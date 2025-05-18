from requests import get, patch
import json, hashlib

cardNumber = "0107a5de48a35bcc6d03535d00478e29e089a92f1104ac5d40efb5bdfb2435d4"

def write_data():
  auth_url = "https://wtechhk.com/wbank/v2/csrftoken"
  token = get(url=auth_url, headers={"Authorization": "Bearer wtech666"}).json()["token"]
  r = get(url="https://wtechhk.com/wbank/auth/v1/session", data={"user": "benchan609", "pw": "Chan1234#", "url": "/wbank/card/action", "csrf_token": token})
  if r.status_code != 200: print(r)
  data = json.dumps(r.json(), indent=4)
  with open("data.json", "w") as w:
    w.write(data)
    w.close()

def wpay_payment():
  with open("data.json", "r") as fp:
    data = json.load(fp)
    data["password"] = data["loginPw"]
    data["cardNumber"] = hashlib.sha256(f"{data['accnumber']}->{data['password']}".encode("utf-8")).hexdigest()
    data["accessKey"] = "0988"
    data["reviewer"] = "boc.hk"
    data["amount"] = "1000"
    pmReq = patch(url="https://wtechhk.com/wbank/card/action", json=data)
    if pmReq.status_code != 200: print(pmReq.json())
    else: print(pmReq.json())
    fp.close()
write_data()
"""
url = "https://wtechhk.com/wbank/card/action"
data = {"cardNumber": cardNumber,
        "password": "Chan1234#",
        "accessKey": "09988",
        }
resp = get(url=url)
if resp.status_code != 200: print(resp)
else: 
  password = resp.json()["loginPw"]
  paymentData = {"cardNumber": cardNumber, "password": password, "accessKey": "0988", "reviewer": "wbank", "amount": "100"}
  res = patch(url=url, json=paymentData, headers={"Content-Type": "application/json"})
  if res.status_code != 200: print(res)
  else: print(res.json())
  """