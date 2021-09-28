
from db import db
from repositories.threads import threads_repository

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

    def username_taken(self, username):
        sql = "SELECT :username IN (SELECT username from users) as bool;"
        result = db.session.execute(sql, {"username": username})
        return result.fetchone().bool


        

users_repository = UsersRepository()