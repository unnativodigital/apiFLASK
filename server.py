from flask import Flask, request, jsonify

app = Flask(__name__)
todos = []

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def post_todos():
    # Verificar si se ha recibido un cuerpo de solicitud
    if request.json is None:
        return jsonify({'error': 'Solicitud inválida. Se requiere un cuerpo JSON.'}), 400  # Bad Request
    
    data = request.json
    
    # Validación de entrada
    if 'id' not in data or 'tarea' not in data:
        return jsonify({'error': 'Solicitud inválida. Se requiere "id" y "tarea".'}), 400  # Bad Request

    # Verificar si ya existe una tarea con el mismo id
    if any(todo['id'] == data['id'] for todo in todos):
        return jsonify({'error': 'Ya existe una tarea con ese ID.'}), 409  # Conflict
    
    # Añadir la tarea a la lista
    todos.append(data)  
    return jsonify(data), 201  # Created

@app.route('/todos', methods=['DELETE'])
def delete_todos():
    data = request.json
    
    # Validación de entrada
    if not data or 'id' not in data:
        return jsonify({'error': 'Solicitud inválida. Se requiere "id".'}), 400  # Bad Request
    
    # Filtra las tareas y elimina la que tiene el id especificado
    initial_length = len(todos)
    todos[:] = [todo for todo in todos if todo.get('id') != data['id']]
    
    if len(todos) == initial_length:
        return jsonify({'error': 'Tarea no encontrada.'}), 404  # Not Found
    
    return jsonify({'message': 'Tarea eliminada'}), 204  # No Content

if __name__ == '__main__':
    app.run(host='localhost', port=5004, debug=True)
