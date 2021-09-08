
from db import db

class ThreadsRepository:
    def __init__(self):
        pass

    def create_a_thread(self, community_id, title, content):
        sql = "INSERT INTO threads (community_id, title, content) VALUES (:community_id, :title, :content)"
        db.session.execute(sql, {"community_id": community_id, "title":title, "content":content})
        db.session.commit()

    def get_threads(self, community_name):
        sql = "SELECT * from threads INNER JOIN communities ON threads.community_id = communities.id WHERE communities.name = :community_name"
        result = db.session.execute(sql, {"community_name": community_name })
        return result.fetchall()

    def get_thread(self, thread_id):
        sql = "SELECT * from threads WHERE threads.id = :thread_id"
        result = db.session.execute(sql, {"thread_id": thread_id})
        return result.fetchone()

    def get_messages(self, thread_id):
        sql = "SELECT * from thread_messages WHERE thread_messages.thread_id = :thread_id"
        result = db.session.execute(sql, {"thread_id": thread_id})
        return result.fetchall()

    def add_message(self, thread_id, user_id, content):
        sql = "INSERT INTO thread_messages (thread_id, user_id, content) VALUES (:thread_id, :user_id, :content)"
        db.session.execute(sql, {"thread_id": thread_id, "user_id": user_id, "content": content})
        db.session.commit()

    def get_votes(self, thread_id):
        sql = "SELECT SUM(vote) AS votes FROM threads_to_users WHERE threads_to_users.thread_id = :thread_id"
        result = db.session.execute(sql, {"thread_id": thread_id})
        return result.fetchone()

    def upvote(self, thread_id, user_id):
        sql = "UPDATE threads_to_users SET vote=1 WHERE threads_to_users.user_id=:user_id AND threads_to_users.thread_id = :thread_id"
        db.session.execute(sql, {"thread_id": thread_id, "user_id": user_id})
        db.session.commit()

    def downvote(self, thread_id, user_id):
        sql = "UPDATE threads_to_users SET vote=-1 WHERE threads_to_users.user_id=:user_id AND threads_to_users.thread_id = :thread_id"
        db.session.execute(sql, {"thread_id": thread_id, "user_id": user_id})
        db.session.commit()

    def check_that_vote_exists(self, thread_id, user_id):
        sql = "SELECT user_id FROM threads_to_users WHERE thread_id=:thread_id AND user_id=:user_id"
        result = db.session.execute(sql, {"thread_id": thread_id, "user_id": user_id})
        if result.fetchone() == None:
            sql = "INSERT INTO threads_to_users (user_id, thread_id, vote) VALUES (:user_id, :thread_id, 0)"
            db.session.execute(sql, {"thread_id": thread_id, "user_id": user_id})
            db.session.commit()


threads_repository = ThreadsRepository()