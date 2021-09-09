
from repositories.users import (users_repository as default_users_repository)
from repositories.threads import (threads_repository as default_threads_repository)
from werkzeug.security import check_password_hash, generate_password_hash
from db import db


class UsersService:
    def __init__(self,users_repository=default_users_repository,
                threads_repository=default_threads_repository):
        self._users_repository = users_repository
        self._threads_repository = threads_repository

    def get_user_by_name(self, username):
        return self._users_repository.get_user_by_name(username)

    def login(self, username, password):
        user = self._users_repository.get_user_by_name(username)
        if user:
            hash_value = user.password
            if check_password_hash(hash_value, password):
                return True
        
        return False

    def create_user(self, username, password):
        hash_value = generate_password_hash(password)
        self._users_repository.create_user(username, hash_value)

    def get_threads(self, username):
        user = self._users_repository.get_user_by_name(username)
        return self._threads_repository.get_user_threads(user.id)

users_service = UsersService()