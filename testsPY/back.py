from flask import Flask, jsonify
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)

config = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME")
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**config)
        return connection

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erro: Nome de usuário ou senha incorretos.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Erro: O banco de dados não existe.")
        else:
            print(f"Erro inesperado: {err}")
        return None

@app.route('/clientes', methods=['GET'])
def get_clientes():
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "falha ao conectar com o banco"}), 500
    
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM clientes")
    resultados = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(resultados)

if __name__ == '__main__':
    app.run(host='localhost', port=5000)