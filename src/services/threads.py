from repositories.threads import (threads_repository as default_threads_repository)
from repositories.communities import (communities_repository as default_communities_repository)

class ThreadsService:
    def __init__(self,threads_repository=default_threads_repository,
                communities_repository=default_communities_repository):
        self._threads_repository = threads_repository
        self._communities_repository = communities_repository

    def create_a_thread(self, community_name, title, content):
        community = self._communities_repository.get_community(community_name)
        self._threads_repository.create_a_thread(community.id, title, content)

    def get_thread(self, thread_id):
        return self._threads_repository.get_thread(thread_id)

threads_service = ThreadsService()