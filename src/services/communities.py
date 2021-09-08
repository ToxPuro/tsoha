
from repositories.communities import (communities_repository as default_communities_repository)

class CommunitiesService:
    def __init__(self,communities_repository=default_communities_repository):
        self._communities_repository = communities_repository

    def create_community(self, name, description):
        self._communities_repository.create_community(name, description)

    def get_communities_user_not_in(self,username):
        return self._communities_repository.get_communities_user_not_in(username)

communities_service = CommunitiesService()