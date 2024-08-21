from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Database configuration
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'todo'
app.config['MYSQL_HOST'] = 'localhost'

mysql = MySQL(app)

@app.route('/todos', methods=['GET'])
def get_todos():
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todos")
    todos = cursor.fetchall()
    todos_list = [{'id': todo[0], 'title': todo[1]} for todo in todos]
    return jsonify(todos_list)

@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.json
    title = data['title']
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (title) VALUES (%s)", (title,))
    conn.commit()
    return jsonify({'message': 'Todo created'}), 201

@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    data = request.json
    title = data['title']
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("UPDATE todos SET title = %s WHERE id = %s", (title, id))
    conn.commit()
    return jsonify({'message': 'Todo updated'})

@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id = %s", (id,))
    conn.commit()
    return jsonify({'message': 'Todo deleted'})

if __name__ == '__main__':
    app.run(debug=True)
