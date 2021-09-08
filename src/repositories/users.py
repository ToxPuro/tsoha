
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

    def get_thread_vote(self, user_id, thread_id):
        threads_repository.check_that_vote_exists(user_id, thread_id)
        sql = "SELECT vote FROM threads_to_users WHERE threads_to_users.user_id=:user_id AND threads_to_users.thread_id = :thread_id"
        result = db.session.execute(sql, {"user_id":user_id, "thread_id": thread_id})
        return result.fetchone()
        

users_repository = UsersRepository()