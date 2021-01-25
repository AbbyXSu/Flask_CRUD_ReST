# #main.py
# #from flask import Flask
# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello World!'

# import some modules and set up a route for the path /item/new:

# to run : FLASK_APP=main.py flask run


from .helper import add_to_list
from.helper import get_all_items
from .helper import getone_item
from.helper import update_status
from.helper import delete_item
from os import error
#import helper
from flask import Flask, request, Response
import json

app= Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello World !"

@app.route("/item", methods =["POST"])
def add_item():
    #get item from the POST body
    #The request module is used to parse the request and get HTTP body data or the query parameters from the URL.
    req_data=request.get_json()
    item = req_data["item"]

    # Add item to the List 
    res_data = add_to_list(item)
    # Response is used to return a response to the client. The response is of type JSON.
    #return error if item not added 
    #a status of 400 if the item was not added due to some client error. 
    if res_data is None:
        err = {
            'error': f'item not added - {item}'
        }
        response = Response (json.dumps(err), status =400, mimetype = "application/json")
        return response 
    #return response 
    #The json.dumps() function converts the Python object or dictionary into a valid JSON object.
    response = Response(json.dumps(res_data),mimetype ="application/json")

@app.route('/items/all')
def getall_items():
    #refer to getting the helper.get_all_items()
    res_data = get_all_items()
    response= Response (json.dumps(res_data), mimetype="application/json")
    return response

#Getting a individual Item
#it needs the route to accept a GET request
# and the item name should be submitted as a query parameter.
#A query parameter is passed in the format ?name=value with the URL. 
#e.g. http://base-url/path/to/resource/?name=value
# If there are spaces in the value 
#you need to replace them with either + or with %20(URL-encoded version of a space)
#& character:seperating multiple name-value pairs(arguments)
@app.route('/item/status', methods=["GET"])
def get_one_item():
## Get parameter from the URL
    item_name = request.args.get("name")
#Get items from helper
    status =getone_item(item_name)
#Return 404 if not found 
    if status is None:
        err = {
            'error': f'item not found - {item_name}'
        }
        response = Response (json.dumps(err), status =404, mimetype = "application/json")
        return response 
# Return status
    res_data = {
        'status': status
    }
    response = Response(json.dumps(res_data), status=200, mimetype='application/json')
    return response

@app.route('/item/update', methods=["Put"])
def updateStatus():
#Get items from the POST body
    req_data = request.get_json()
    item = req_data["item"]
    status = req_data["status"]
    res_data =update_status(item,status)

#Return error if the status could not be updated/none
    if not res_data:
        response = Response("{'error': 'Error updating item - '" + item + ", " + status+"}", status=400 , mimetype='application/json')
        return response
      # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')

    return response

@app.route('/item/remove', methods=['DELETE'])
def deleteItem():
    # Get item from the POST body
    req_data = request.get_json()
    item = req_data['item']

    # Delete item from the list
    res_data = delete_item(item)

    # Return error if the item could not be deleted
    if res_data is None:
        response = Response("{'error': 'Error deleting item - '" + item +  "}", status=400 , mimetype='application/json')
        return response

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')
    return response