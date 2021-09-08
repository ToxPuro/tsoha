
from repositories.communities import (communities_repository as default_communities_repository)

class CommunitiesService:
    def __init__(self,communities_repository=default_communities_repository):
        self._communities_repository = communities_repository

    def create_community(self, name, description):
        self._communities_repository.create_community(name, description)

communities_service = CommunitiesService()