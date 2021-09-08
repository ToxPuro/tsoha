
from repositories.users import (users_repository as default_users_repository)
from werkzeug.security import check_password_hash, generate_password_hash
from db import db


class UsersService:
    def __init__(self,users_repository=default_users_repository):
        self._users_repository = users_repository

    def get_tags(self):
        if self._login_service.is_authenticated():
            return self._tag_repository.get_tags(self._login_service.current_user())
        else:
            return []

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

users_service = UsersService()