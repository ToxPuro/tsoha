from db import db

class CommunitiesRepository:
    def __init__(self):
        pass

    def create_community(self, name, description):
        sql = "INSERT INTO communities (name, description) VALUES (:name, :description)"
        db.session.execute(sql, {"name":name, "description":description})
        db.session.commit()

communities_repository = CommunitiesRepository()