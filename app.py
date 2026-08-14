from flask import Flask, request, jsonify, render_template, session, redirect
from flask_socketio import SocketIO
from mysql.connector import pooling

# =========================================================
# FLASK APP
# =========================================================
app = Flask(__name__)

app.secret_key = "greenhouse_secret_key"

# =========================================================
# SOCKET IO
# =========================================================
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="threading"
)

# =========================================================
# DATABASE
# =========================================================
dbconfig = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "greenhouses"
}

pool = pooling.MySQLConnectionPool(
    pool_name="greenhouse_pool",
    pool_size=5,
    **dbconfig
)

# =========================================================
# LIVE SENSOR VALUES
# =========================================================
latest = {
    "ultrasonic": None,
    "temp": None,
    "hum": None,
    "soil": None,
    "light": None,
    "motion": None
}

# =========================================================
# EMIT LIVE DATA
# =========================================================
def emit_snapshot():

    print("EMITTING:", latest)

    socketio.emit(
        "sensor_snapshot",
        latest
    )

# =========================================================
# DATABASE INSERT
# =========================================================
def insert_data(sensor_type, v1, v2=None):

    conn = pool.get_connection()

    cursor = conn.cursor()

    sql = """
    INSERT INTO sensor_data
    (
        sensor_type,
        value1,
        value2,
        status
    )
    VALUES (%s,%s,%s,%s)
    """

    cursor.execute(sql, (sensor_type, v1, v2, "OK"))

    conn.commit()

    cursor.close()
    conn.close()

# =========================================================
# ULTRASONIC
# =========================================================
@app.route('/api/ultrasonic', methods=['POST'])
def ultrasonic():

    d = request.json

    latest["ultrasonic"] = float(d.get("distance", 0))

    insert_data(
        "ultrasonic",
        latest["ultrasonic"]
    )

    emit_snapshot()

    return jsonify({
        "success": True
    })

# =========================================================
# SOIL
# =========================================================
@app.route('/api/soil', methods=['POST'])
def soil():

    d = request.json

    latest["soil"] = float(d.get("moisture", 0))

    insert_data(
        "soil",
        latest["soil"]
    )

    emit_snapshot()

    return jsonify({
        "success": True
    })

# =========================================================
# PIR MOTION
# =========================================================
@app.route('/api/pir', methods=['POST'])
def pir():

    d = request.json

    latest["motion"] = int(d.get("motion", 0))

    insert_data(
        "pir",
        latest["motion"]
    )

    emit_snapshot()

    return jsonify({
        "success": True
    })

# =========================================================
# DHT22
# =========================================================
@app.route('/api/dht', methods=['POST'])
def dht():

    data = request.get_json()

    if not data:

        return jsonify({
            "success": False,
            "message": "No JSON received"
        }), 400

    try:

        temp = float(data.get("temperature", 0))
        hum = float(data.get("humidity", 0))

        latest["temp"] = temp
        latest["hum"] = hum

        insert_data(
            "temp_hum",
            temp,
            hum
        )

        emit_snapshot()

        return jsonify({
            "success": True,
            "temperature": temp,
            "humidity": hum
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# =========================================================
# LDR
# =========================================================
@app.route('/api/ldr', methods=['POST'])
def ldr():

    data = request.json

    print("LDR RECEIVED:", data)

    raw = float(data.get("ldr_raw", 0))

    percent = float(data.get("light_percent", 0))

    status = data.get("status", "Unknown")

    # SAVE PERCENT FOR DASHBOARD
    latest["light"] = percent

    # DATABASE
    insert_data(
        "ldr",
        raw,
        percent
    )

    # SEND LIVE UPDATE
    emit_snapshot()

    return jsonify({
        "success": True,
        "raw": raw,
        "percent": percent,
        "status": status
    })
# =========================================================
# LOGIN CHECK
# =========================================================
def protected():

    return session.get("logged_in")

# =========================================================
# LOGIN PAGE
# =========================================================
@app.route('/login', methods=['GET'])
def login_page():

    return render_template("login.html")

# =========================================================
# LOGIN API
# =========================================================
@app.route('/login', methods=['POST'])
def login_user():

    data = request.json

    username = data.get("username")
    password = data.get("password")

    conn = pool.get_connection()

    cursor = conn.cursor(dictionary=True)

    sql = """
    SELECT * FROM workers
    WHERE username=%s AND password=%s
    """

    cursor.execute(sql, (username, password))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:

        session["logged_in"] = True
        session["username"] = user["username"]
        session["role"] = user["role"]

        return jsonify({
            "success": True,
            "user": user["fullname"],
            "role": user["role"]
        })

    return jsonify({
        "success": False,
        "message": "Invalid credentials"
    }), 401

# =========================================================
# SIGNUP PAGE
# =========================================================
@app.route('/signup', methods=['GET'])
def signup_page():

    return render_template("signup.html")

# =========================================================
# SIGNUP API
# =========================================================
@app.route('/signup', methods=['POST'])
def signup_user():

    data = request.json

    conn = pool.get_connection()

    cursor = conn.cursor()

    # CHECK USERNAME
    check_sql = """
    SELECT * FROM workers
    WHERE username=%s
    """

    cursor.execute(check_sql, (data['username'],))

    existing = cursor.fetchone()

    if existing:

        cursor.close()
        conn.close()

        return jsonify({
            "success": False,
            "message": "Username already exists"
        })

    # INSERT
    sql = """
    INSERT INTO workers
    (
        fullname,
        employee_id,
        email,
        phone,
        role,
        username,
        password
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        data['fullname'],
        data['employeeid'],
        data['email'],
        data['phone'],
        data['role'],
        data['username'],
        data['password']
    )

    cursor.execute(sql, values)

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "success": True
    })

# =========================================================
# DASHBOARD
# =========================================================

@app.route('/')
def dashboard():

    if not protected():
        return redirect('/login')

    return render_template("dashboard.html")

# =========================================================
# PAGES
# =========================================================
@app.route('/motion')
def motion_page():

    if not protected():
        return redirect('/login')

    return render_template("motion.html")

@app.route('/light')
def light_page():

    if not protected():
        return redirect('/login')

    return render_template("light.html")

@app.route('/water_level')
def water_level_page():

    if not protected():
        return redirect('/login')

    return render_template("water_level.html")

@app.route('/dht')
def dht_page():

    if not protected():
        return redirect('/login')

    return render_template("temp_hum.html")

@app.route('/soil')
def soil_page():

    if not protected():
        return redirect('/login')

    return render_template("soil.html")
@app.route('/home') 
def home():
     if not protected(): 
        return redirect('/login') 
     return render_template("home.html")

# =========================================================
# LOGOUT
# =========================================================
@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')


# =========================================================
# SOCKET CONNECT
# =========================================================
@socketio.on("connect")
def connected():

    print("CLIENT CONNECTED")

    emit_snapshot()

# =========================================================
# START APP
# =========================================================
if __name__ == "__main__":

    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=False
    )