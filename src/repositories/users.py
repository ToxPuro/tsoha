
from db import db

class UsersRepository:
    def __init__(self):
        pass
    
    def get_user_by_name(self,username):
        sql = "SELECT id, password FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username":username})
        return result.fetchone()    

users_repository = UsersRepository()