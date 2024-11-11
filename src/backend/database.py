from db import db

def insert_message(msg):
    sql = "INSERT INTO messages (msg, timestamp) VALUES (:msg, NOW())"
    db.session.execute(sql, {"msg":msg})
    db.session.commit()
