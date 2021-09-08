
from repositories.communities import (communities_repository as default_communities_repository)
from repositories.users import (users_repository as default_users_repository)
from repositories.threads import (threads_repository as default_threads_repository)

class CommunitiesService:
    def __init__(self,communities_repository=default_communities_repository,
                users_repository=default_users_repository,
                threads_repository = default_threads_repository):

        self._communities_repository = communities_repository
        self._users_repository = users_repository
        self._threads_repository = threads_repository

    def create_community(self, name, description, username):
        self._communities_repository.create_community(name, description)
        self.join_community(name, username)
        self.add_admin(name, username)

    def get_communities_user_not_in(self,username):
        return self._communities_repository.get_communities_user_not_in(username)
    
    def get_communities_user_in(self,username):
        return self._communities_repository.get_communities_user_in(username)

    def get_community(self, community_name):
        return self._communities_repository.get_community(community_name)

    def join_community(self, community_name, username):
        community = self.get_community(community_name)
        user = self._users_repository.get_user_by_name(username)
        self._communities_repository.join_community(community.id, user.id)

    def add_admin(self, community_name, username):
        community = self.get_community(community_name)
        user = self._users_repository.get_user_by_name(username)
        self._communities_repository.add_admin(community.id, user.id)

    def get_threads(self, community_name):
        return self._threads_repository.get_threads(community_name)

communities_service = CommunitiesService()