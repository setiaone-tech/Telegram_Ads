import mysql.connector

mydb = mysql.connector.connect(
  host="",
  user="",
  password="",
  database=""
)

def getBotToken():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT bot_token FROM integration")
    myresult = mycursor.fetchone()
    # Memeriksa apakah ada hasil
    if myresult:
        return myresult[0]  # Mengembalikan bot_token dari hasil
    else:
        return None  # Jika tidak ada hasil

def getWebApp():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT web_app FROM integration")
    myresult = mycursor.fetchone()
    # Memeriksa apakah ada hasil
    if myresult:
        return myresult[0]  # Mengembalikan web_app dari hasil
    else:
        return None  # Jika tidak ada hasil

def getInte():
    mycursor = mydb.cursor()

    query = "SELECT * FROM integration"
    mycursor.execute(query)
    myresult = mycursor.fetchone()
    if myresult:
        return myresult  # Mengembalikan web_app dari hasil
    else:
        return None  # Jika tidak ada hasil

def updateInte(token=None, webapp=None, tags=None, min=None):
    mycursor = mydb.cursor()
    
    # Mengecek apakah data sudah ada
    check_sql = "SELECT COUNT(*) FROM integration WHERE bot_token IS NOT NULL AND web_app IS NOT NULL"
    mycursor.execute(check_sql)
    result = mycursor.fetchone()
    
    if result and result[0] > 0:
        # Jika data sudah ada, lakukan UPDATE
        sql = "UPDATE integration SET bot_token = %s, web_app = %s, min_wd = %s, js_tags = %s"
        values = (token, webapp, min, tags)
        mycursor.execute(sql, values)
        mydb.commit()
    else:
        # Jika data belum ada, lakukan INSERT
        insert_sql = "INSERT INTO integration (bot_token, web_app, min_wd, js_tags) VALUES (%s, %s, %s, %s)"
        values = (token, webapp, min, tags)
        mycursor.execute(insert_sql, values)
        mydb.commit()

def getTask():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM tasks")
    myresult = mycursor.fetchall()
    # Memeriksa apakah ada hasil
    if myresult:
        return myresult  # Mengembalikan web_app dari hasil
    else:
        return []  # Jika tidak ada hasil

def insertTask(link=None, jenis=None, reward=None):
    mycursor = mydb.cursor()
    insert_sql = "INSERT INTO tasks (link, jenis, reward) VALUES (%s, %s, %s)"
    values = (link, jenis, reward)
    mycursor.execute(insert_sql, values)
    mydb.commit()

def updateTask(id, link, jenis, reward):
    mycursor = mydb.cursor()
    # Jika data sudah ada, lakukan UPDATE
    sql = "UPDATE tasks SET link = %s, jenis = %s, reward = %s WHERE task_id = %s"
    values = (link, jenis, reward, id)
    mycursor.execute(sql, values)
    mydb.commit()

def deleteTask(uid):
    mycursor = mydb.cursor()

    # Menggunakan parameterized query untuk menghindari SQL Injection
    sql = "DELETE FROM tasks WHERE task_id = %s"
    values = (uid,)  # Tambahkan koma untuk membuatnya menjadi tuple
    mycursor.execute(sql, values)
    mydb.commit()

def getPayment():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT payments.payment_id, users.username, payments.reward, payments.jenis_payment, payments.tujuan, payments.status FROM payments INNER JOIN users ON payments.user_id = users.user_id")
    myresult = mycursor.fetchall()
    # Memeriksa apakah ada hasil
    if myresult:
        return myresult  # Mengembalikan web_app dari hasil
    else:
        return []  # Jika tidak ada hasil
    
def updatePayment(payid, status):
    mycursor = mydb.cursor()

    if status == "Success":
        # Ambil reward dari tabel payments berdasarkan payment_id (payid)
        sql = "SELECT reward, user_id FROM payments WHERE payment_id = %s"
        mycursor.execute(sql, (payid,))
        payment_data = mycursor.fetchone()

        # Jika data tidak ditemukan, beri respons error
        if payment_data is None:
            print("Payment not found!")
            return

        payment_reward = payment_data[0]  # reward dari payments
        user_id = payment_data[1]  # user_id yang terkait

        # Ambil reward dari tabel users berdasarkan user_id
        sql = "SELECT reward FROM users WHERE user_id = %s"
        mycursor.execute(sql, (user_id,))
        user_data = mycursor.fetchone()

        # Jika data user tidak ditemukan, beri respons error
        if user_data is None:
            print("User not found!")
            return

        user_reward = user_data[0]  # reward dari users

        # Pastikan hasil pengurangan tidak negatif
        if user_reward < payment_reward:
            print("Insufficient user reward to deduct!")
            return

        # Jika cukup, kurangi reward dari users
        new_user_reward = user_reward - payment_reward

        # Update nilai reward di tabel users
        sql = "UPDATE users SET reward = %s WHERE user_id = %s"
        mycursor.execute(sql, (new_user_reward, user_id))
        mydb.commit()

    # Update status pembayaran di tabel payments
    sql = "UPDATE payments SET status = %s WHERE payment_id = %s"
    values = (status, payid)
    mycursor.execute(sql, values)
    mydb.commit()

    print("Payment status updated and user reward deducted.")


def getPayments(payid):
    mycursor = mydb.cursor()
    query = "SELECT payments.payment_id, users.telegram_id, users.username, payments.reward, payments.jenis_payment, payments.tujuan, payments.status FROM payments INNER JOIN users ON payments.user_id = users.user_id WHERE payments.payment_id = %s"
    mycursor.execute(query, (payid,))
    myresult = mycursor.fetchall()
    
    # Memeriksa apakah ada hasil
    if myresult:
        return myresult  # Mengembalikan hasil
    else:
        return []  # Jika tidak ada hasil

    # Menutup cursor setelah selesai
    mycursor.close()

def insertPayment(tele_id, amount, acc=None, pay=None):
    mycursor = mydb.cursor()
    query = "SELECT * FROM users WHERE telegram_id = %s"
    mycursor.execute(query, (tele_id,))
    user = mycursor.fetchone()
    if user[3] == None:
        query = "UPDATE users SET account_number = %s, jenis = %s WHERE telegram_id = %s"
        val = (acc, pay, tele_id)
        mycursor.execute(query, val)
    else:
        acc = user[3]
        pay = user[4]
    history_query = "INSERT INTO payments (user_id, reward, jenis_payment, tujuan, status) VALUES (%s, %s, %s, %s, %s)"
    history_val = (user[0], amount, pay, acc, "Pending")
    mycursor.execute(history_query, history_val)
    mydb.commit()

def getUsers():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM users")
    myresult = mycursor.fetchall()
    # Memeriksa apakah ada hasil
    if myresult:
        return myresult  # Mengembalikan web_app dari hasil
    else:
        return []  # Jika tidak ada hasil

def getInfoUser(uid):
    mycursor = mydb.cursor()
    query = "SELECT u.user_id, u.reward AS user_reward, t.task_id, t.link, t.jenis, t.reward AS task_reward FROM users u LEFT JOIN tasks t ON 1=1 WHERE u.telegram_id = %s AND ( t.jenis != 'Join Channel' OR NOT EXISTS ( SELECT 1 FROM history h WHERE h.user_id = u.user_id AND h.task_id = t.task_id ) );"
    mycursor.execute(query, (uid,))
    myresult = mycursor.fetchall()
    
    # Memeriksa apakah ada hasil
    if myresult:
        return myresult  # Mengembalikan hasil
    else:
        return []  # Jika tidak ada hasil

def getInfoUsers(uid):
    mycursor = mydb.cursor()
    query = "SELECT * FROM users WHERE telegram_id = %s"
    val = (uid,)
    mycursor.execute(query, val)
    myresult = mycursor.fetchone()

    if myresult:
        return myresult
    else:
        return []

def insertHistory(uid, task_id):
    mycursor = mydb.cursor()

    # Step 1: Ambil poin dari tasks.reward berdasarkan task_id
    query = "SELECT reward FROM tasks WHERE task_id = %s"
    mycursor.execute(query, (task_id,))
    task_reward = mycursor.fetchone()

    if task_reward:
        # Step 2: Ambil poin dari users.reward
        task_reward = task_reward[0]  # task_reward adalah tuple, ambil nilai reward
        query = "SELECT user_id, reward FROM users WHERE telegram_id = %s"
        mycursor.execute(query, (uid,))
        user_reward = mycursor.fetchone()

        if user_reward:
            new_poin = user_reward[1]  # user_reward adalah tuple, ambil nilai reward

            # Update reward di users dengan menambahkan task_reward
            new_reward = new_poin + task_reward
            update_query = "UPDATE users SET reward = %s WHERE telegram_id = %s"
            mycursor.execute(update_query, (new_reward, uid))

            # Step 3: Insert data ke tabel history
            history_query = "INSERT INTO history (user_id, task_id, status) VALUES (%s, %s, %s)"
            history_val = (user_reward[0], task_id, "Claimed")
            mycursor.execute(history_query, history_val)
            mydb.commit()

            print("History inserted and reward updated successfully.")
        else:
            print("User not found.")
    else:
        print("Task not found.")

    mycursor.close()

def getUser(tele_id):
    mycursor = mydb.cursor()
    query = "SELECT * FROM users WHERE telegram_id = %s"
    mycursor.execute(query, (tele_id,))
    myresult = mycursor.fetchone()
    # Memeriksa apakah ada hasil
    if myresult:
        return myresult  # Mengembalikan web_app dari hasil
    else:
        return []  # Jika tidak ada hasil

def getHistory(tele_id):
    mycursor = mydb.cursor()
    query = "SELECT * FROM payments WHERE user_id IN (SELECT user_id FROM users WHERE telegram_id = %s)"
    mycursor.execute(query, (tele_id,))
    myresult = mycursor.fetchall()
    # Memeriksa apakah ada hasil
    if myresult:
        return myresult  # Mengembalikan web_app dari hasil
    else:
        return []  # Jika tidak ada hasil

def getTotalWD():
    mycursor = mydb.cursor()
    query = "SELECT SUM(reward) AS total_reward FROM payments WHERE status = 'Success'"
    mycursor.execute(query)
    myresult = mycursor.fetchone()
    if myresult:
        return myresult
    else:
        return []
    
def regisUser(username, tele_id, fingerprint):
    mycursor = mydb.cursor()
    
    # Mengecek apakah fingerprint atau telegram_id sudah ada di database
    query = "SELECT * FROM users WHERE fingerprint = %s OR telegram_id = %s"
    val = (fingerprint, tele_id)
    mycursor.execute(query, val)
    
    # Mengambil satu baris hasil query
    myresul = mycursor.fetchone()

    # Jika sudah ada hasil, artinya user sudah terdaftar
    if myresul is not None:
        return "Anda sudah mendaftar/sudah terdaftar!"
    else:
        # Menyimpan user baru jika tidak ada yang terdaftar
        query = "INSERT INTO users (username, telegram_id, fingerprint) VALUES (%s, %s, %s)"
        val = (username, tele_id, fingerprint)
        mycursor.execute(query, val)
        mydb.commit()
        
        # Menutup cursor dan koneksi (baik jika menggunakan koneksi manual)
        mycursor.close()
        
        return "Anda berhasil mendaftar."

def delUser(uid):
    mycursor = mydb.cursor()
    
    try:
        # Hapus data dari tabel payments terlebih dahulu
        query = "DELETE FROM payments WHERE user_id = %s"
        val = (uid,)
        mycursor.execute(query, val)
        
        # Hapus data dari tabel history
        query = "DELETE FROM history WHERE user_id = %s"
        mycursor.execute(query, val)
        
        # Hapus data dari tabel users terakhir
        query = "DELETE FROM users WHERE user_id = %s"
        mycursor.execute(query, val)
        
        # Commit perubahan ke database
        mydb.commit()
        print("Data user dan relasi berhasil dihapus.")
        
    except mysql.connector.Error as err:
        # Jika ada kesalahan, batalkan transaksi
        mydb.rollback()
        print(f"Terjadi kesalahan: {err}")
    
    # Tutup cursor
    mycursor.close()


def getTotalWdUser():
    mycursor = mydb.cursor()
    query = "SELECT u.username, u.telegram_id, SUM(p.reward) AS total_withdraw FROM users u JOIN payments p ON u.user_id = p.user_id WHERE p.status = 'Success' GROUP BY u.username, u.telegram_id"
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    if myresult:
        return myresult
    else:
        return []