from app import app
from flask import request
from .models import User, Character

# - - - - - - - - - - - - - - - - - - - - - -
@app.route("/", methods = ['GET'])
def home():
    return {'available routes':[
        {'user':[
            "/user/create",
            "/user/update",
            "/user",

        ]}, {
            'character': [
                '/add',
                "/update",
                "/delete/<character_id>"
            ]
        }
    ]}
# - - - - - - - - - - - - - - - - - - - - -
@app.route("/add", methods = ['POST'])
def add():
    payload = request.json
    user = User.query.filter_by(token=request.headers['Authorization'].split()[-1]).first()
    if not user:
        return {
            'status': 'not ok',
            'message': "That token does not belong to a valid user"
        }
    name = payload['name']
    description = payload['description'] 
    comics = payload['comics']
    power = payload['power']
    c = Character(name, description, comics, power, user.id)
    c.save_to_db()
    return {
        'status': 'ok',
        'message': 'Succesfully added character to your collection.'
    }



@app.route("/update", methods = ['POST'])
def update():
    payload = request.json
    user = User.query.filter_by(token=request.headers['Authorization'].split()[-1]).first()
    if not user:
        return {
            'status': 'not ok',
            'message': "That token does not belong to a valid user"
        }
    fields = payload['fields']
    c = Character.query.get(payload['character_id'])
    if c:
        for field in fields:
            if field == 'name':
                c.name = payload[field]
            elif field == 'description':
                c.description = payload[field]
            elif field == 'power':
                c.power = payload[field]
            elif field == 'comics_appeared_in':
                c.comics_appeared_in = payload[field]
            else:
                print('invalid field', field)
        c.save_changes()
            
    return {'status': 'ok'}

@app.route("/delete/<int:character_id>", methods = ['DELETE'])
def delete(character_id):
    user = User.query.filter_by(token=request.headers['Authorization'].split()[-1]).first()
    if not user:
        return {
            'status': 'not ok',
            'message': "That token does not belong to a valid user"
        }
    c = Character.query.get(character_id)
    if c:
        c.delete_from_db()
    return {'status':'ok',
            'message': 'Successfully deleted!'
                    }
#  - - - - - - USER- - - - - - - -
@app.route("/user", methods = ['GET'])
def get_user():
    return {'test':'test'}

@app.route("/user/create", methods = ['POST'])
def create_user():
    payload = request.json
    name = payload['name']
    email = payload['email']
    password = payload['password']
    print(payload)
    user = User(name, email, password)
    user.save_to_db()
    return {'message':'Successfully created user!'}

@app.route("/user/update", methods = ['POST'])
def user_update():
    return {'test':'test'}

