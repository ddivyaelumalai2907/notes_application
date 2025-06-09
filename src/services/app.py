import pathlib, sys, os

root_path = pathlib.Path(__file__).parent.resolve().parent.resolve()
sys.path.append(str(root_path))

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

import json, yaml
from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dao import notes,user,sample_notes
import re
from flask import session
from model.notes import Notes
from model.user import User
from flask import render_template

# Read DB config and create engine
file_config = yaml.load(open(os.path.join(root_path, "..", "conf", "config.yml")), Loader=yaml.SafeLoader)
db_engine = create_engine(file_config['db_connection_string'], pool_size=50, isolation_level="READ COMMITTED")

app = Flask(__name__,template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = "d2c8b3b7827be24fb307a5248d86d741" 

def get_db_connection():
    Session = sessionmaker(bind=db_engine)
    return Session()

@app.route('/add/user',methods=['POST'])
def register_user():
    res = {
        'status' : 'success',
        'message' : 'User is registered successfully',
        'data' : None
    }

    try :
        data =  request.get_json(force=True)

        if 'name' not in  data:
            res['status'] = 'failure'
            res['message'] = 'No user name given'
            return json.dumps(res) 
        
        if 'email' not in data:
            res['status'] = 'failure'
            res['message'] = 'No email id given'
            return json.dumps(res)
        
        if 'password' not in data:
            res['status'] = 'failure'
            res['message'] = 'No password given'
            return json.dumps(res)
        
        valid_email = is_valid_email(data['email'])
        if not valid_email:
            res['status'] = 'failure'
            res['message'] = 'Please give the vaild Email id'
            return json.dumps(res)

        vaild_password = is_valid_password(data["password"])
        if not vaild_password:
                res['status'] = 'failure'
                res['message'] = 'Please give the vaild password of 1 Upper case,1 lower case 1 dugit 1 special character of minimum length 5'
                return json.dumps(res)
        
        connection = get_db_connection()
        res['data'] = user.new_user(
            name = (data['name']).strip(),
            email = (data['email']).strip(),
            password = (data['password']).strip(),
            connection = connection
        )
        session['user_id'] = res['data']
        get_sample_notes()
    except Exception as e:
        print(str(e))
        res['status'] = 'failuer'
        res['message'] = 'unable to register the user'
        connection.rollback()
    
    return json.dumps(res)

@app.route('/login_user', methods=['POST'])
def login_user():
    res = {
        'status' : 'success',
        'message' : 'User Logined sucessfully',
        'data' : None
    }

    try :
        data =  request.get_json(force=True)
        if 'email' not in data:
            res['status'] = 'failure'
            res['message'] = 'No email id given'
            return json.dumps(res)
        
        if 'password' not in data:
            res['status'] = 'failure'
            res['message'] = 'No password given'
            return json.dumps(res)

        valid_email = is_valid_email(data['email'])
        if not valid_email:
            res['status'] = 'failure'
            res['message'] = 'Please give the vaild Email id'
            return json.dumps(res)

        vaild_password = is_valid_password(data["password"])
        if not vaild_password:
            res['status'] = 'failure'
            res['message'] = 'Please give the vaild password of 1 Upper case,1 lower case 1 dugit 1 special character of minimum length 5'
            return json.dumps(res)
        
        connection = get_db_connection()
        result = user.user_exist(
            email = (data['email']).strip(),
            password = (data['password']).strip(),
            connection = connection
        )
        if not result:
            res['status'] = 'failuer'
            res['message'] = 'the user does not exists. please register!'
        else:
            session['user_id'] = result['user_id']
            session['user_name'] = result['user_name']
            return json.dumps(res) 

    except Exception as e:
        print(str(e))
        res['status'] = 'failuer'
        res['message'] = 'unable to register the user'
    return render_template('login.html', error=res['message'])

# rendering login.html
@app.route('/login')
def login():
    return render_template('login.html')

# rendering register.html
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/update/password',methods = ['POST'])
def update_user():
    res = {
        'status' : 'success',
        'message' : None,
        'data' : None
    }
    try :
        data =  request.get_json(force=True)
        if 'email' not in data:
            res['status'] = 'failure'
            res['message'] = 'No email id given'
            return json.dumps(res)

        if 'new_password' not in data:
            res['status'] = 'failure'
            res['message'] = 'No new password given'
            return json.dumps(res)

        vaild_new_password = is_valid_password(data['new_password'])
        if not vaild_new_password:
            res['status'] = 'failure'
            res['message'] = 'Please give the vaild new password of 1 Upper case,1 lower case 1 dugit 1 special character of minimum length 5'
            return json.dumps(res)

        valid_email = is_valid_email(data['email'])
        if not valid_email:
            res['status'] = 'failure'
            res['message'] = 'Please give the vaild Email id'
            return json.dumps(res)
        
        connection = get_db_connection()
        result = user.update_user_data(
            email = (data['email']).strip(),
            connection = connection,
            new_password = (data.get('new_password')),
        )
        if len(result) == 0:
            res['status'] = 'failuer'
            res['message'] = 'the given user details cannot be updated!'
        else:
            if 'msg' in result:
                res['status'] = 'failuer'
                res['message'] = 'the given user details already present!'
            else:
                res['data'] = result['user_id']
                res['message'] = 'User password is updated successfully'
                
    except Exception as e:
        print(str(e))
        res['status'] = 'failure'
        res['message'] = 'unable to update the user data'
        connection.rollback()
    return  json.dumps(res)

@app.route('/add/note', methods=['POST'])
def add_new_note():
    res = {
        'status': 'success',
        'message': None,
        'data': None
    }

    try:
        data = request.json
        title = data.get('title')
        content = data.get('content')

        if 'title' not in data:
            res['status'] = 'failure'
            res['message'] = 'No title given'
            return json.dumps(res)
        
        if 'content' not in data:
            res['status'] = 'failure'
            res['message'] = 'No content given'
            return json.dumps(res)

        connection = get_db_connection()
        res['data'] = notes.add_notes(
            title=title,
            content=content,
            user_id = session.get('user_id'),
            connection=connection
        )

    except Exception as e:
        print("Error:", str(e))
        res['status'] = 'failure'
        res['message'] = 'Unable to add note'
        connection.rollback()

    return  json.dumps(res)

@app.route('/update/note', methods=['POST'])
def add_update_note():
    res = {
        'status': 'success',
        'message':'Note Upadted sucessfully',
        'data': None
    }

    try:
        data =  request.get_json(force=True)
        if 'note_id' not in data:
            res['status'] = 'failure'
            res['message'] = 'No note id given'
            return json.dumps(res)
        if 'update_to' not in data:
            res['status'] = 'failure'
            res['message'] = 'Not given what to update'
            return json.dumps(res)
        if  data['update_to'] == "title":
            if 'new_title' not in data:
                res['status'] = 'failure'
                res['message'] = 'No title given'  
                return json.dumps(res)  
        if  data['update_to'] == "content":
            if 'new_content' not in data:
                res['status'] = 'failure'
                res['message'] = 'No content given'
                return json.dumps(res)
        if  data['update_to'] == "both":
            if 'new_title' not in data:
                res['status'] = 'failure'
                res['message'] = 'No title given'
                return json.dumps(res)
            if 'new_content' not in data:
                res['status'] = 'failure'
                res['message'] = 'No content given'
                return json.dumps(res)

        connection = get_db_connection()
        notes.update_note(
            note_id = (data.get('note_id', {}).get('noteId')),
            connection = connection,
            new_title = (data.get('new_title')),
            new_content = (data.get('new_content'))
        )
    except Exception as e:
        print(str(e))
        res['status'] = 'failure'
        res['message'] = 'unable to upadte the user data'
        connection.rollback()
    return json.dumps(res)

@app.route("/delete/note", methods=["POST"])
def delete_note():
    res = {
        'status': 'success',
        'message': 'Note deleted succesfully',
        'data': None
    }
    try:
        data = request.get_json()
        if 'note_id' not in data:
            res['status'] = 'failure'
            res['message'] = 'Please give the note_id'
            return json.dumps(res)
        note_id = data.get("note_id")
        connection = get_db_connection()
        notes.delete_note(note_id = note_id,connection = connection)
    except Exception as e:
        print("Error:", str(e))
        res['status'] = 'failure'
        res['message'] = 'Unable to add note'
        connection.rollback()

    return json.dumps(res)
    
def user_notes():
    res = {
        'status': 'success',
        'message': 'Notes for this user {}'.format(session.get('user_id')),
        'data': None
    }
    try:
        user_id = session.get('user_id')
        connection = get_db_connection()
        all_notes = notes.get_all_user_notes(
            user_id = user_id,
            connection = connection
        )
        if len(all_notes)>0:
           res['data'] = all_notes

    except Exception as e:
        print(str(e))
        res['status'] = 'failure'
        res['message'] = 'unable to notes for the user {}'.format(session.get('user_id'))
    return json.dumps(res)

@app.route('/dashboard')
def dashboard():
    res = {
        'status': 'success',
        'message': 'Notes for this user {}'.format(session.get('user_id')),
        'data': None
    }
    try:
        user_id = session.get('user_id')
        user_name = session.get('user_name')
        all_notes = user_notes()
        fetched_notes = json.loads(all_notes)
        if fetched_notes['status'] == 'success':
            if  len(fetched_notes['data']) > 0:
                res['mesage'] = 'There is a note for specific user'
                res['data'] = fetched_notes['data']
        else:
            res['message'] = 'There is not notes for the specific user please create it'
    except Exception as e:
        print(str(e))
        res['status'] = 'failure'
        res['message'] = 'unable to notes for the user {}'.format(session.get('user_id'))
    return render_template('dashboard.html',res = res,user_name = user_name)

@app.route('/notes', methods=['GET'])
def get_sample_notes():
    res = {
        'status': 'success',
        'message': 'Sample Noted fetched sucessfully',
        'data': None
    }
    try:
        user_id = session.get('user_id')
        connection = get_db_connection()
        res['data'] = sample_notes.get_all_sample_notes(
            connection = connection
        )
    except Exception as e:
        print(str(e))
        res['status'] = 'failure'
        res['message'] = 'unable to get the sample notes'

    return render_template("home.html", notes=res)
       
def is_valid_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$', email)

def is_valid_password(password):
    return re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{5,}$', password)

if __name__ == '__main__':
   app.run(debug=True)
