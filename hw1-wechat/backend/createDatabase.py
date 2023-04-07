import sqlite3

dbConn=sqlite3.connect("wechat.db")

def initDB():

    # Initialize users
    SQL="""CREATE TABLE users(
        user_id integer PRIMARY KEY autoincrement,
        username text NOT NULL UNIQUE,
        password text NOT NULL,
        avatar_dirct text NOT NULL
    )
    """
    dbConn.execute(SQL)

    # Initialize friends
    SQL="""CREATE TABLE friends(
        CONSTRAINT user_fk1 FOREIGN KEY (user_id) REFERENCES users (user_id),
        CONSTRAINT user_fk2 FOREIGN KEY (user_id) REFERENCES users (user_id),
    )
    """
    dbConn.execute(SQL)


    # Initialize Stocks Table
    SQL="""CREATE TABLE groups(
        group_id integer PRIMARY KEY autoincrement,
        groupname text NOT NULL
    )
    """
    dbConn.execute(SQL)

    ### Initialize Price Tables
    SQL="""CREATE TABLE group_members(
        group_id unsigned,
        user_id unsigned,
        PRIMARY KEY (group_id, user_id),
        CONSTRAINT group_users_fk1 FOREIGN KEY (group_id) REFERENCES groups (group_id),
        CONSTRAINT group_users_fk2 FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    """
    dbConn.execute(SQL)

    SQL="""CREATE TABLE messages(
        message_id bigint unsigned auto_increment PRIMARY KEY,
        user_id unsigned,
        message text,
        time smalldatetime,
        CONSTRAINT messages_fk1 FOREIGN KEY (group_id) REFERENCES groups (group_id)
    )
    """
    dbConn.execute(SQL)

initDB() ## Only runs once


dbConn.close()