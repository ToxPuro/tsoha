
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

threads_repository = ThreadsRepository()