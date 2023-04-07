#登录，验证，用户信息相关的函数

from urllib import request
from flask import make_response, Blueprint, Flask,request,render_template, redirect,jsonify, url_for, Blueprint
from __main__ import dbConn, app
from flask_jwt_extended import (
        JWTManager, jwt_required, create_access_token,
        get_jwt_identity
    )


#helper 函数，用来查询是否有此用户名的用户
def find_username(username):
    SQL = f'''SELECT u.user_id, u.username, u.password, u.avatar
        FROM users u
        WHERE u.username = "{username}"
        '''
    user = dbConn.execute(SQL)
    
    column_names = [col[0] for col in user.description]
    row = user.fetchall()
    if not row:
        return None


    #因为用户名称是独一无二的，因此可以直接flatten 获得第一个数据

    #返回一个字典
    temp_d = dict(zip(column_names, row[0]))  

    print(temp_d)

    return temp_d

#往数据库中添加一个用户
def insert_user(user):
    SQL=f"""insert into users(username, password, avatar)
    values('{user["username"]}', '{user["password"]}', {user["avatar"]})
    """
    dbConn.execute(SQL)
    dbConn.commit()


# 登录逻辑
@app.route('/api/login', methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    #先查找是否输入正确
    user = find_username(username)
    
    if not user or not user["password"] == password:
        return jsonify({
            "status": "failed",
            "message": "Failed getting user"
        }), 401
        
    # 生成一个访问的token
    access_token = create_access_token(identity=username)
    
    return jsonify({
        "status": "success",
        "message": "login successful",
        "data": {
            "id": user["user_id"],
            "token": access_token,
            "username": user["username"],
            "avatar": user["avatar"]
        }
    }), 200

#注册用户逻辑
@app.route('/api/signup', methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    avatar = data.get("avatar")
    #查看用户名是否已经存在
    user = find_username(username)
    #用户存在
    if user is not None:
            return make_response( jsonify({'message': 'Account {} already exists'.format(data['username']), 'status':'failure'}))
    #两次输入的密码不同
    elif (data.get("password") != data.get("cpassword")):
            return make_response( jsonify({'message': 'Passwords dont match','status':'failure'}))
    else: #可以注册
        new_user = {"username":username, "password":password, "avatar": avatar }
        insert_user(new_user)
            
        return jsonify({
            "status": "success",
            "message": "User added successfully"
        }), 201

#登出逻辑，实际上未使用
@app.route('/api/logout', methods=["POST"])
def logout():
    return 'Logout'

