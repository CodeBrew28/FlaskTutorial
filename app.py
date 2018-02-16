from flask import Flask, jsonify, request
import mockdb.mockdb_interface as db

app = Flask(__name__)

def create_response(data={}, status=200, message=''):
    """
    Wraps response in a consistent format throughout the API
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response

    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself
    """
    response = {
        'success': 200 <= status < 300,
        'code': status,
        'message': message,
        'result': data
    }
    return jsonify(response), status

"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""

@app.route('/')
def hello_world():
    return create_response('hello world!')

@app.route('/mirror/<name>')
def mirror(name):
    data = {
        'name': name
    }
    return create_response(data)

# TODO: Implement the rest of the API here!
@app.route('/users')
def get_all_users():
    team_name = request.args.get('team')
    if not team_name:
        return create_response(db.get('users'))
    all_users = db.get('users')
    matched_users = [user for user in all_users if user['team'] == team_name]
    data = {'users': matched_users}
    return create_response(data)

@app.route('/users/<id>')
def get_user_by_id(id):
    return create_response(db.getById('users', int(id)))

@app.route('/users', methods=['POST'])
def post_user():
    name = request.form.get('name')
    age = request.form.get('age')
    team = request.form.get('team')
    data = {}
    if name and age and team:
        payload = {'name': name, 'age':age, 'team': team}
        data = db.create('users', payload)
        return create_response(data, status=201)

    else:
        return create_response(data, 422, 'user name, age and team must be provided')

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):    
    name = request.form.get('name')
    age = request.form.get('age')
    team = request.form.get('team')
    data = {}
    if name:
        data['name'] = name
    if age:
        data['age'] = age
    if team:
        data['team'] = team
    response = db.updateById('users', int(id), data)
    if not response:
        return create_response({}, 404, 'user not found')
    return create_response(response, 201)

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):    
    if not db.getById('users', int(id)):
        return create_response({}, 404, 'user not found')
    db.deleteById('users', int(id))
    return create_response({}, 200, 'delete success')
    

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == '__main__':
    app.run(debug=True)
