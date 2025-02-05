from flask import Flask, jsonify, request
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

@app.route('/clientes', methods=['POST'])
def clientAdd():
    
    connection = get_db_connection()

    dados = request.json
    name = dados.get('name')
    email = dados.get('email')

    cursor = connection.cursor(dictionary=True)

    sql = "INSERT INTO clientes (nome, email) VALUES (%s, %s)"
    valores = (name, email)

    cursor.execute(sql, valores)
    connection.commit()
    
    cursor.close()
    connection.close()

    return jsonify({
        "mensagem": "Cliente inserido com sucesso!"
    }), 201

@app.route('/clientes/<int:id>', methods=['DELETE'])
def clienteDel(id):

    connection = get_db_connection()

    cursor = connection.cursor(dictionary=True)

    sql = "DELETE FROM clientes WHERE id = %s"
    valores = (id,)

    cursor.execute(sql, valores)
    connection.commit()

    cursor.close()
    connection.close()
    
    return jsonify({"message": "Excluido com sucesso!"}), 200


if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)