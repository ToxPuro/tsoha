from db import db

class CommunitiesRepository:
    def __init__(self):
        pass

    def create_community(self, name, description):
        sql = "INSERT INTO communities (name, description) VALUES (:name, :description)"
        db.session.execute(sql, {"name":name, "description":description})
        db.session.commit()

    def get_communities_user_not_in(self, username):
        sql = "SELECT DISTINCT name, description FROM communities LEFT JOIN community_users ON communities.id = community_users.community_id LEFT JOIN users ON users.id = community_users.user_id WHERE users.username != :username OR users.username IS NULL"
        result = db.session.execute(sql, {"username": username})
        return result.fetchall()

    def get_communities_user_in(self,username):
        sql = "SELECT DISTINCT name, description FROM communities INNER JOIN community_users ON communities.id = community_users.community_id INNER JOIN users ON users.id = community_users.user_id WHERE users.username = :username"
        result = db.session.execute(sql, {"username": username})
        return result.fetchall()

    def get_community(self, community_name):
        sql = "SELECT * from communities WHERE communities.name = :community_name"
        result = db.session.execute(sql, {"community_name": community_name})
        return result.fetchone()

    def join_community(self, community_id, user_id):
        sql = "INSERT INTO community_users (community_id, user_id) VALUES (:community_id, :user_id)"
        db.session.execute(sql, {"community_id": community_id, "user_id": user_id})
        db.session.commit()

    def add_admin(self, community_id, user_id):
        sql = "UPDATE community_users SET admin=TRUE WHERE community_users.community_id=:community_id AND community_users.user_id = :user_id"
        db.session.execute(sql, {"community_id": community_id, "user_id": user_id})
        db.session.commit()

communities_repository = CommunitiesRepository()