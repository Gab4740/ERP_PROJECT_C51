from flask import Flask, request, jsonify
import subprocess
import sqlite3
from config import DB_PATH

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  
    return conn

@app.route('/login', methods=['POST'])
def login():
    print("here")
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT visibilite FROM info_LOGIN WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return jsonify({'success': True, 'role': user['visibilite']})
    else:
        return jsonify({'success': False}), 401

if __name__ == '__main__':
    app.run(debug=True)