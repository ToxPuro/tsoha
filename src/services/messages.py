from repositories.threads import (threads_repository as default_threads_repository)
from repositories.users import (users_repository as default_users_repository)
from repositories.communities import (communities_repository as default_communities_repository)
from repositories.messages import (messages_repository as default_messages_repository)

class MessagesService:
    def __init__(self,threads_repository=default_threads_repository,
                communities_repository=default_communities_repository,
                users_repository = default_users_repository,
                messagess_repository = default_messages_repository):
        self._threads_repository = threads_repository
        self._communities_repository = communities_repository
        self._users_repository = users_repository
        self._messages_repository = messagess_repository

    def upvote(self, message_id, user_id):
        self._messages_repository.upvote(message_id, user_id)

    
    def downvote(self, message_id, user_id):
        self._messages_repository.downvote(message_id, user_id)

    def delete(self, message_id):
        self._messages_repository.delete(message_id)

messages_service = MessagesService()