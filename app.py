

import json
import uuid
import boto3
from flask import (Flask,
                   jsonify,
                   make_response,
                   request)



app = Flask(__name__)
client = boto3.client(
    'dynamodb',
    region_name='us-east-1',
    aws_access_key_id='xxxxxxxxxxxxxxxx',
    aws_secret_access_key='xxxxxxxxxxx'
)



# Settings
app.config['REQUEST_METHOD_POST']  = 'POST'
app.config['REQUEST_METHOD_GET']  = 'GET'
app.config['REQUEST_METHOD_DELETE']  = 'DELETE'
app.config['BAD_REQUEST_MESSEGE'] = ({
    'status':'error', 'messege':'Missing parameters in request'
})


@app.route("/api/v1/user/",methods = ['GET','POST','DELETE','PUT'])
def user_controller() -> (json):
    
    if (request.method == app.config['REQUEST_METHOD_POST']):
        
        # Si el metodo es post , se encargaria
        # de crear un nuevo usuario
        
        email = request.form.get('email',None)
        userName = request.form.get('userName',None)
        userId = str(uuid.uuid4()).replace('-','')
        
        if email and userName:
            client.put_item(
                TableName='usersTable',
                Item=({ 'id':{ 'S':userId },'name':{ 'S':userName },'email':{ 'S':email } })
            )
            return ({ 'status':'ok' })
        
        return (app.config['BAD_REQUEST_MESSEGE'],400)
        
    
    if (request.method == app.config['REQUEST_METHOD_GET']):
        
        # Si el metodo es get , se encargaria
        # de mostrar todos los usuarios
        
        userItems = client.scan(TableName='usersTable')['Items']
        responseUsers = []
        
        for user in userItems:
            responseUsers.append({
                'id':user['id']['S'],
                'name':user['name']['S'],
                'email':user['email']['S']
            })

        return ({ 'status':'ok', 'data':responseUsers })



@app.route('/api/v1/user/<userId>',methods=[ 'GET','DELETE' ])
def user_controller_join(userId) -> (json):
    
    if request.method == app.config['REQUEST_METHOD_GET']:
        
        # Si el metodo es get , se encargaria
        # obtener el usuario por su id
        
        user = client.get_item(TableName='usersTable',Key={ 'id':{ 'S':userId } })
        user = user.get('Item')
        
        if user:
            return ({
                'status':'ok',
                'user':{
                    'id':user['id']['S'],
                    'name':user['name']['S'],
                    'email':user['email']['S'],
                }
            })
            
        return ({ 'status':'error', 'messege':'The user not fount' },400)
    
    
    if request.method == app.config['REQUEST_METHOD_DELETE']:
        
        # Si el metodo es delete , se encargaria
        # de eliminar el usuario por su id
        
        client.delete_item(TableName='usersTable',Key={ 'id':{ 'S':userId } })
        return ({ 'status':'ok' })
        
        



@app.errorhandler(404)
def resource_not_found(e) -> (str):
    return make_response(jsonify(error='Not found!'), 404)


