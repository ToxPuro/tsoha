
from db import db

class MessagesRepository:
    def __init__(self):
        pass

    def upvote(self, message_id, user_id):
        self.check_that_vote_exists(message_id, user_id)
        sql = "UPDATE messages_to_users SET vote=1 WHERE messages_to_users.user_id=:user_id AND messages_to_users.message_id = :message_id"
        db.session.execute(sql, {"message_id": message_id, "user_id": user_id})
        db.session.commit()

    def downvote(self, message_id, user_id):
        self.check_that_vote_exists(message_id, user_id)
        sql = "UPDATE messages_to_users SET vote=-1 WHERE messages_to_users.user_id=:user_id AND messages_to_users.message_id = :message_id"
        db.session.execute(sql, {"message_id": message_id, "user_id": user_id})
        db.session.commit()

    def check_that_vote_exists(self, message_id, user_id):
        sql = "SELECT user_id FROM messages_to_users WHERE message_id=:message_id AND user_id=:user_id"
        result = db.session.execute(sql, {"message_id": message_id, "user_id": user_id})
        if result.fetchone() == None:
            sql = "INSERT INTO messages_to_users (user_id, message_id, vote) VALUES (:user_id, :message_id, 0)"
            db.session.execute(sql, {"message_id": message_id, "user_id": user_id})
            db.session.commit()

    def delete(self, message_id):
        sql = "DELETE FROM thread_messages WHERE id=:message_id"
        db.session.execute(sql, {"message_id":message_id})
        db.session.commit()

    def edit(self, message_id, new_content):
        sql = "UPDATE thread_messages SET content=:new_content, edited=TRUE WHERE id=:message_id"
        db.session.execute(sql, {"message_id": message_id, "new_content": new_content})
        db.session.commit()

    def get_message(self, message_id):
        sql = "SELECT * from thread_messages WHERE id=:message_id"
        result =db.session.execute(sql, {"message_id" : message_id})
        return result.fetchone()



messages_repository = MessagesRepository()