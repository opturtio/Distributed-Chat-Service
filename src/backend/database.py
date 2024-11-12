from db import db

def insert_message(msg):
    sql = "INSERT INTO messages (msg, timestamp) VALUES (:msg, NOW())"
    db.session.execute(sql, {"msg":msg})
    db.session.commit()

def insert_peer(user_id, name, ip):
    sql = "INSERT INTO peers (user_id, name, ip) VALUES (:user_id, :name, :ip) VALUES ()"
    db.session.execute(sql, {"user_id":user_id, "name":name, "ip":ip})
    db.session.commit()

def fetch_peers():
    sql = "SELECT * FROM peers"
    result = db.session.execute(sql)
    return result.fetchall()