
from db import db

class UsersRepository:
    def __init__(self):
        pass
    
    def get_user_by_name(self,username):
        sql = "SELECT id, password FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username":username})
        return result.fetchone()

    def create_user(self, username, hash_value):
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()

users_repository = UsersRepository()