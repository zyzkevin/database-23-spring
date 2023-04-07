#后端主要逻辑

from flask import Flask,request,render_template, redirect,jsonify, url_for, make_response
import json
import random
import base64

import sqlite3

from flask_cors import CORS
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from flask_jwt_extended import (
        JWTManager, jwt_required, create_access_token,
        get_jwt_identity
    )

dbConn=sqlite3.connect("wechat.db", check_same_thread=False)
app=Flask("__name__")

#import auth components
import auth

app.config['SECRET_KEY'] = 'yzxyzxyzx'
CORS(app, resources={r"/*": {"origins": "*"}})
jwt = JWTManager(app)
#socketio 实现实时通讯
socketio = SocketIO(app, cors_allowed_origins="*", logger=True)

#获取存储在数据库中的所有 可用头像，用于用户注册时候选择
@app.route('/api/profiles', methods=['GET'])
def profiles():

    
    SQL=f"""SELECT *
    FROM U_Avatars
    ORDER BY id
    """
    #使用排序保证所有的都是顺序的
    
    avats = dbConn.execute(SQL)
    avats = avats.fetchall()

    message = [{
        "id": i[0],
        "avat_dat": base64.encodebytes(i[1]).decode('ascii') #必须传输base64 才能jsonify response
    } for i in avats]

    return make_response(jsonify(message))
    
#socketeio 传输过来实时通讯，发送一个message
@app.route('/', methods=['POST'])
@socketio.on('event')
def message(json):    
    from_user = json.get('from_user')
    to_group = json.get('to_group')
    message = json.get('message')
    timestamp = json.get('timestamp')
    filee = json.get("file") #一个bool值，1 时代表为文件，2则是普通信息
    #发送的空信息
    if to_group == None:
        return make_response(jsonify({"message":"failed"}))
    SQL=f"""insert into messages(user_id, message, time, group_id, file)
    values({from_user}, "{message}", "{timestamp}", {to_group}, {filee})
    """
    dbConn.execute(SQL)
    dbConn.commit()

    message = {
        "from_user": from_user,
        "to_group": to_group,
        "message": message,
        "time": timestamp,
    }
    #helper 函数获得最新的聊天记录
    msg = getMsg(to_group)


    #返回一个callback给前端，实现发出信息后本地也能及时看见
    socketio.emit('RESPONSE', msg, callback=messageReceived) 
    return make_response(jsonify(message))

# 获取一个聊天群的 聊天记录的函数，基本功能为join message 信息和用户信息，并且返回
def getMsg(group_id):
    SQL=f"""SELECT *
    FROM U_Avatars
    ORDER BY id
    """
    #使用排序保证所有的都是顺序的
    
    avats = dbConn.execute(SQL)
    avats = avats.fetchall()

    message = [{
        "id": i[0],
        "avat_dat": base64.encodebytes(i[1]).decode('ascii')
    } for i in avats]

    #合并message计略和用户信息
    SQL = f"""SELECT m.message_id, m.user_id, m.message, m.time, m.group_id, u.avatar, u.username, m.file
    FROM messages m 
    LEFT JOIN users u ON m.user_id = u.user_id
    WHERE m.group_id = {group_id}"""

    msgs = dbConn.execute(SQL)
    msgs = msgs.fetchall()
    
    return [
        {
            "id": msg[0],
            "message": msg[2],
            "to_group": msg[4],
            "time": msg[3],
            "from_user": msg[1],
            "avatar": message[msg[5] - 1]["avat_dat"],
            "from_username": msg[6],
            "file": msg[7]
        }
        for msg in msgs
    ]
@jwt_required
@app.route('/api/get_message/<group_id>')
def getRoomMsgs(group_id):
   return jsonify(getMsg(group_id))

#获得用户所在的所有群聊的信息。
@jwt_required
@app.route('/api/groups/<user_id>', methods=["GET"])
def groupList(user_id):
    #获取当前用户id所在的群们
    SQL = f'''SELECT g.groupname, g.group_id
        FROM group_members gm 
        LEFT JOIN groups g ON gm.group_id = g.group_id
        WHERE gm.user_id = {user_id}
        '''
    
    groups = dbConn.execute(SQL)
    groups = groups.fetchall()

    G_dict = [
        {"group_id": group[1], "groupname": group[0]} for group in groups ]
    #在用户参与的每个群都获得这些群的信息
    for group in G_dict:
        g_id = group["group_id"]
        SQL = f'''SELECT u.username, u.user_id, u.avatar
        FROM group_members gm 
        LEFT JOIN users u ON u.user_id = gm.user_id
        WHERE gm.group_id = {g_id}
        '''
        users = dbConn.execute(SQL)
        users = users.fetchall()

        group["username"] = [i[0] for i in users]
        group["user_id"] = [i[1] for i in users]
        group["avatar"] = [i[2] for i in users]


    #获取所有群聊中用户的基础信息
    
    print("groups:", G_dict)
    return make_response(jsonify(
    G_dict
), 200)


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')    


#获得用户的好友列表
@jwt_required
@app.route('/api/friends/<user_id>', methods=["GET"])
def Gettingfriends(user_id):
    #获取用户id
    print()
    SQL = f'''SELECT users.user_id, users.username, users.avatar
        FROM users 
        LEFT JOIN friends ON friends.friend_id = users.user_id
        WHERE friends.base_id = {user_id}
        '''
    
    friends = dbConn.execute(SQL)
    friends = friends.fetchall()
    
    
    print(friends)
    return make_response(jsonify(
    [{"id": user[0], "userName": user[1], "avatar": user[2]} for user in friends]
), 200)


#checking 是否有incoming friend 申请
@jwt_required
@app.route('/api/friendpends/<user_id>', methods=["GET"])
def UserList(user_id):
    print(user_id)
    #获取用户id
    SQL = f'''SELECT users.user_id, users.username, users.avatar
        FROM users 
        LEFT JOIN friends ON friends.base_id = users.user_id
        WHERE friends.friend_id = {user_id} AND friends.pending = 1
        '''
    
    friends = dbConn.execute(SQL)
    friends = friends.fetchall()
    
    
    print("friend request", friends)
    return make_response(jsonify(
    [{"id": user[0], "userName": user[1], "avatar": user[2]} for user in friends]
), 200)

#确认好友申请，update对方数据的同时己方也添加记录
@jwt_required
@app.route('/api/confirmFriend', methods=["POST"])
def confirm():
    data = request.get_json()
    from_user = data.get("from_user")
    to_user = data.get("to_user") #输入应当为用户名
    print("confriming", data)
    #adding to own db, pending = false
    SQL=f"""insert into friends(base_id, friend_id, pending)
    values('{to_user}', '{from_user}', 0)
    """
    dbConn.execute(SQL)
    dbConn.commit()


    # updating friend's db
    SQL=f"""UPDATE friends
    SET pending = false
    WHERE base_id = {from_user} AND friend_id = {to_user}
    """
    dbConn.execute(SQL)
    dbConn.commit()

    return make_response(jsonify({"message": "Friend Confirmed! 开始聊天！"}
), 200)


@jwt_required
@app.route('/api/createGroup', methods=["POST"])
def createGroup():
    data = request.get_json()
    group_mem_ids = data.get("group_mems")
    group_name = data.get("group_name")

    #adding to own db, pending = false
    SQL=f"""insert into groups(groupname)
    values('{group_name}')
    """
    dbConn.execute(SQL)
    dbConn.commit()

    #get id of last inserted

    SQL=f"""SELECT last_insert_rowid()"""
    group_id = dbConn.execute(SQL)
    group_id=group_id.fetchall()[0][0]

    print(group_mem_ids)
    #adding to own db, pending = false
    for i in group_mem_ids:
        SQL=f"""insert into group_members(group_id, user_id)
        values({group_id}, {i})
        """
        dbConn.execute(SQL)
        dbConn.commit()

    SQL = f"""insert into messages(user_id, message, time, group_id)
    values({group_mem_ids[0]}, '现在可以开始聊天了！', "1", {group_id})"""
    dbConn.execute(SQL)
    dbConn.commit()

    return make_response(jsonify({"message":"已经通知对方！"}
), 200)

#好友申请，需要先判断用户名是否合法，再判断是否已经为好友，最后才能发出申请
@jwt_required
@app.route('/api/addfriend', methods=["POST"])
def addFriend():
  
    data = request.get_json()
    from_user = data.get("from_user")
    to_user = data.get("to_user") #输入应当为用户名

    #查看用户是否存在
    SQL = f'''SELECT u.user_id, u.username, u.avatar
        FROM users u
        WHERE u.username = '{to_user}'
        '''
    to_user_dat = dbConn.execute(SQL)
    to_user_data = to_user_dat.fetchall()


    if len( to_user_data) == 0:
        return make_response( jsonify({'message': 'User {} does not exist!'.format(to_user), 'status':'failure'}))

    #查看用户是否已经是好友了
    SQL = f'''SELECT users.user_id, users.username
        FROM users 
        LEFT JOIN friends ON friends.friend_id = users.user_id
        WHERE friends.base_id = {from_user} AND
        users.username = '{to_user}'
        '''
    
    friends = dbConn.execute(SQL)
    friends = friends.fetchall()


    if len(friends)!=0:
        return make_response( jsonify({'message': 'User {} is already a friend!'.format(to_user), 'status':'failure'}))

    #如果上述都不成立，则可以发出好友申请请求
    SQL=f"""insert into friends(base_id, friend_id, pending)
    values({from_user}, {to_user_data[0][0]}, 1)
    """
    dbConn.execute(SQL)
    dbConn.commit()


    print(friends)
    return make_response(jsonify({
        'message': f"Friend Request Sent to {to_user}!"
    }), 200)



#不适用的时候关闭和数据库的连接
@app.teardown_appcontext
def shutdown_session(exception=None):
    #dbConn.close()
    pass 

if __name__ == "__main__":
    #from gevent import monkey
    #monkey.patch_all(select=True, socket=True)
    socketio.run(app, debug=True)  #FOR REMOVE SOCKETIO WARNING
    #app.run(host="localhost", port=80, debug=True)
