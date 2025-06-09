from model import user
from operator import and_

def new_user(name,email,password,connection):
    obj = user.User(user_name=name,user_email=email,password=password)
    connection.add(obj)
    connection.commit()
    return  obj.user_id
    connection.rollback()

def user_exist(email,password,connection):
    obj = connection.query(user.User).filter(
    and_(
        user.User.user_email == email,
        user.User.password == password
    )).first()

    if obj is not None:
        return {
            'user_name':obj.user_name,
            'user_id':obj.user_id
        }
    return False

def update_user_data(email,connection,new_password):
    data = {}
    obj = connection.query(user.User).filter(
        user.User.user_email == email
    ).first()

    if obj is not None:
        if obj.password == new_password:
            data['msg'] = 'The given password is already present'
            return data
        obj.password = new_password
        connection.commit()
        data['user_id'] = obj.user_id
        data['password_upadte'] = True
 
    return data