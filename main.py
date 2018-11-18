import firebase_admin
from firebase_admin import db, firestore, credentials
import flask 
import json


# Copy and paste the content of the credentials JSON file between the quotes
credJSON = """

"""

# Convert the JSON string into a python dictionary
credDict = json.loads(credJSON, strict=False)

# Load credentials dictionary
cred = credentials.Certificate(credDict)

# Initialize firebase connection
firebase_admin.initialize_app(cred, options={
    'databaseURL': 'https://<DB-NAME>.firebaseio.com'
})

# List dishes from firebase
def list_dishes():
    dbRef = db.reference('dishes')
    print(dbRef.get())
    return flask.jsonify(dbRef.get())

# List dishes from firestore
def list_dishes_firestore():
    client = firestore.client()
    dishesRef = client.collection('dishes').get()
    dishes=[]
    
    for dish in dishesRef:
        print('{} => {}'.format(dish.id, dish.to_dict()))
        to_dict = dish.to_dict()
        #Assign Id field in object to value of the firestore document Id
        to_dict['id'] = dish.id
        dishes.append(to_dict)
    return flask.jsonify(dishes)

# Add a new dish
def addDish(request):
    req = json.dumps(request.json)
    dictReq = json.loads(req, strict=False)
    client = firestore.client()
    dish = client.collection('dishes').add(dictReq)
    return 'Dish added successfully!'

# Retrieve a specifc dish by Id
def get_dish(id):
    client = firestore.client()
    dish = client.collection('dishes').document(id).get()
    to_dict = dish.to_dict()
    to_dict['id'] = dish.id
    return flask.jsonify(to_dict)

# Delete a dish
def delete_dish(id):
    client = firestore.client()
    dish = client.collection('dishes').document(id).delete()
    return 'Dish deleted successfully!'

# Update a dish
def update_dish(id, request):
    req = json.dumps(request.json)
    dictReq = json.loads(req, strict=False)
    client = firestore.client()
    dish = client.collection('dishes').document(id).set(dictReq)
    return 'Dish updated successfully!'


# Router/Controller
def dishes(request):
    if request.path == '/' or request.path == '':
        if request.method == 'POST':
            return addDish(request)
        elif request.method == 'GET':
            return list_dishes_firestore()
        else:
            return 'Method not supported', 405
    if request.path.startswith('/'):
        id = request.path.lstrip('/')
        if request.method == 'GET':
            return get_dish(id)
        elif request.method == 'DELETE':
            return delete_dish(id)
        elif request.method == 'PUT':
            return update_dish(id, request)
        else:
            return 'Method not supported', 405
    return 'URL not found', 404