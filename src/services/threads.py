from repositories.threads import (threads_repository as default_threads_repository)
from repositories.users import (users_repository as default_users_repository)
from repositories.communities import (communities_repository as default_communities_repository)

class ThreadsService:
    def __init__(self,threads_repository=default_threads_repository,
                communities_repository=default_communities_repository,
                users_repository = default_users_repository):
        self._threads_repository = threads_repository
        self._communities_repository = communities_repository
        self._users_repository = users_repository

    def create_a_thread(self, community_name, username, title, content):
        user = self._users_repository.get_user_by_name(username)
        community = self._communities_repository.get_community(community_name)
        self._threads_repository.create_a_thread(community.id, user.id, title, content)

    def get_thread(self, thread_id, username):
        user = self._users_repository.get_user_by_name(username)
        return self._threads_repository.get_thread(thread_id, user.id)

    def get_messages(self, thread_id, username):
        user = self._users_repository.get_user_by_name(username)
        return self._threads_repository.get_messages(thread_id, user.id)

    def add_message(self, thread_id, user_id, content):
        self._threads_repository.add_message(thread_id, user_id, content)

    def upvote(self, thread_id, user_id):
        self._threads_repository.upvote(thread_id, user_id)

    
    def downvote(self, thread_id, user_id):
        self._threads_repository.downvote(thread_id, user_id)

    def delete_thread(self, thread_id):
        self._threads_repository.delete_thread(thread_id)

threads_service = ThreadsService()