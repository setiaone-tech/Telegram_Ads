from flask import Flask, render_template, redirect, url_for, request, jsonify
import requests, json
import db

app = Flask(__name__)
bot_token = db.getBotToken()
web_app = db.getWebApp()
api_telegram = f"https://api.telegram.org/bot{bot_token}/"

@app.route("/webhook", methods=['GET', 'POST'])
def webhook():
    update = request.get_json()

    if 'message' in update:
        message = update['message']
        chat_id = message['chat']['id']

        # Pesan yang ingin dikirim
        send_text = """
Selamat datang di Ads System Reward!

Ads System Reward adalah bot yang memberikan kamu kesempatan untuk mendapatkan reward hanya dengan menonton iklan. Semakin banyak iklan yang kamu tonton, semakin banyak poin yang kamu kumpulkan, yang nantinya bisa ditukarkan menjadi saldo OVO atau DANA.

Cara Bermain:
• Klik tombol Earn Money Now.
• Tonton iklan yang tersedia.
• Dapatkan poin yang bisa kamu tukarkan dengan saldo OVO atau DANA.

Informasi Penting:
Penarikan minimal adalah 2000 Rupiah.
Penarikan dapat dilakukan melalui OVO dan DANA.

Nikmati pengalaman menonton iklan dan dapatkan rewardmu sekarang!"""

        # Membuat tombol inline
        inline_keyboard = {
            "inline_keyboard": [
                [
                    {"text": "Open Website", "url": web_app}  # Ganti dengan URL yang diinginkan
                ]
            ]
        }

        # Mengirim pesan dengan tombol inline
        sendMessage(chat_id, send_text, inline_keyboard)
        
    return jsonify({"status": "ok"})

def sendMessage(chat_id, text, inline_keyboard=None):
    url = api_telegram + "sendMessage"
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Membuat data pesan yang dikirimkan
    data = {
        "chat_id": chat_id,
        "text": text
    }

    # Menambahkan inline_keyboard hanya jika disediakan
    if inline_keyboard:
        data["reply_markup"] = inline_keyboard

    # Mengirim request untuk mengirim pesan
    response = requests.post(url, headers=headers, json=data)
    return response.json()

@app.route("/", methods=['GET', 'POST'])
def index():
    data = db.getInte()
    return render_template('index.html', data=data)

@app.route("/wd", methods=['GET', 'POST'])
def wd():
    if request.method == "POST":
        tele_id = request.form.get("user_id")
        amount = request.form.get("amount")
        acc = request.form.get("account")
        pay = request.form.get("payment-method")
        db.insertPayment(tele_id, amount, acc, pay)
        return redirect(url_for("index"))
    return render_template('withdraw.html')

@app.route("/del-user", methods=['POST'])
def del_user():
    uid = request.get_json()['uid']
    db.delUser(uid)
    return jsonify({"code": 200, "msg":"success"})

@app.route("/getInfoWD", methods=['POST'])
def infowd():
    tele_id = request.get_json()['tele_id']
    res = db.getUser(tele_id)
    return jsonify({"code": 200, "data":res})

@app.route("/wd-history", methods=['GET', 'POST'])
def wd_history():
    if request.method == "POST":
        tele_id = request.get_json()['tele_id']
        data = db.getHistory(tele_id)
        return jsonify({"code": 200, "data":data})

@app.route("/info", methods=['POST'])
def info():
    user_id = request.get_json()['uid']
    data = db.getInfoUser(user_id)
    return jsonify({"code": 200, "data":data})

@app.route("/info-user", methods=['POST'])
def info_user():
    user_id = request.get_json()['uid']
    data = db.getInfoUsers(user_id)
    return jsonify({"code": 200, "data":data})

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    page = 'dashboard'
    task = db.getTask()
    user = db.getUsers()
    total = db.getTotalWD()
    data = db.getTotalWdUser()
    return render_template("dashboard.html", page=page, task=task, user=user, total=total, data=data)

@app.route("/task", methods=['GET', 'POST'])
def task():
    if request.method == 'POST':
        link = request.get_json()['link']
        jenis = request.get_json()['jenis']
        reward = request.get_json()['reward']
        db.insertTask(link, jenis, reward)
        return jsonify({"code": 200, "msg":"success"})
    page = 'task'
    data = db.getTask()
    return render_template("task.html", page=page, data=data)

@app.route("/task-update", methods=['POST'])
def task_update():
    if request.method == 'POST':
        uid = request.form.get("id")
        link = request.form.get("link")
        jenis = request.form.get("jenis")
        reward = request.form.get("reward")
        db.updateTask(uid, link, jenis, reward)
        return redirect(url_for('task'))

@app.route("/task-delete", methods=['POST'])
def task_delete():
    if request.method == 'POST':
        uid = request.get_json()['id']
        db.deleteTask(uid)
        return jsonify({"code": 200, "msg":"success."})

@app.route("/payment", methods=['GET', 'POST'])
def payment():
    page = 'payment'
    pay = db.getPayment()
    return render_template("payment.html", page=page, pay=pay)

@app.route("/payment-update", methods=['POST'])
def payment_update():
    if request.method == "POST":
        payid = request.get_json()['paymentId']
        status = request.get_json()['status']
        db.updatePayment(payid, status)
        data = db.getPayments(payid)
        send_text =f"""
Withdraw anda sebesar Rp. {data[0][3]} diperbarui statusnya menjadi {data[0][6]}
"""
        sendMessage(data[0][1], send_text)
        return jsonify({"code": 200, "msg":"success"})

@app.route("/users", methods=['GET', 'POST'])
def users():
    page = 'users'
    user = db.getUsers()
    return render_template("users.html", page=page, user=user)

@app.route("/integration", methods=['GET', 'POST'])
def integration():
    if request.method == "POST":
        # Mengambil data dari form
        token = request.form.get('tokenbot')
        webapp = request.form.get('webapp')
        webhook = request.form.get('webhook')
        tags = request.form.get("js-tags")
        min = request.form.get("min-wd")
        
        # Pastikan token dan webapp ada sebelum diproses
        if token or webapp or tags or min:
            db.updateInte(token, webapp, tags, min)
            global bot_token, web_app
            bot_token = db.getBotToken()
            web_app = db.getWebApp()
            getwebhook = requests.get(f"https://api.telegram.org/bot{bot_token}/getWebhookInfo").json()
            if getwebhook['ok'] == True and getwebhook['result']['url'] != webhook:
                update_webhook = requests.get(f"https://api.telegram.org/bot{bot_token}/setWebhook?url={webhook}")
            return redirect(url_for('integration'))  # Redirect ke route yang sama setelah POST

    page = 'integration'
    data = db.getInte()
    return render_template("integration.html", page=page, data=data)

@app.route("/submit", methods=['POST'])
def submit():
    user_id = request.get_json()['user_id']
    task_id = request.get_json()['task_id']

    db.insertHistory(user_id, task_id)
    return jsonify({"code": 200, "msg":"success"})

@app.route("/regis", methods=['POST'])
def regis():
    username = request.get_json()['username']
    telegramId = request.get_json()['telegram_id']
    fingerprint = request.get_json()['fingerprint']
    res = db.regisUser(username, telegramId, fingerprint)
    return jsonify({"code":200, "msg":res})


if __name__ == '__main__':
    app.run(debug=True, port=9000)