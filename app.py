import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, db, initialize_app

# Initialize Flask app
app = Flask(__name__)

# Initialize firebase database
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred, {
    'databaseURL': 'https://test-api-4f85d-default-rtdb.firebaseio.com/'
})

ref = db.reference('tasks')
#e.g. json={'id': '1', 'title': 'Write a blog post'}

@app.route('/list', methods=['GET'])
def read():
    try:
        # Check if ID was passed to URL query
        task_id = request.args.get('id')
        
        if task_id:
            task = ref.child(task_id)
            return jsonify(task.get()), 200
        else:
            tasks = ref.get()
            return jsonify(tasks), 200

    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/add', methods=['POST'])
def create():
    try:
        id = request.json['id']
        task = {
            'id': id,
            'name': request.json['name'],
            'check': False
        }
        ref.child(id).set(task)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/update', methods=['POST', 'PUT'])
def update():
    try:
        id = request.json['id']
        ref.child(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/delete', methods=['GET', 'DELETE'])
def delete():
    try:
        # Check for ID in URL query
        task_id = request.args.get('id')
        ref.child(task_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)