from db import db

class CommunitiesRepository:
    def __init__(self):
        pass

    def create_community(self, name, description):
        sql = "INSERT INTO communities (name, description) VALUES (:name, :description)"
        db.session.execute(sql, {"name":name, "description":description})
        db.session.commit()

    def get_communities(self, user_id):
        sql = "SELECT *,id, (SELECT :user_id IN (SELECT user_id FROM community_users WHERE community_id=id)) AS user_in, (SELECT banned FROM community_users WHERE community_id=id AND user_id=:user_id) AS user_banned from communities";
        result = db.session.execute(sql, {"user_id": user_id})
        return result.fetchall()

    def get_community(self, community_name, user_id):
        sql = "SELECT *, id, (SELECT :user_id IN (SELECT user_id FROM community_users WHERE community_id=id)) AS user_in, (SELECT :user_id IN (SELECT user_id FROM community_users WHERE community_id=id AND community_users.admin=TRUE)) AS user_is_admin from communities WHERE communities.name = :community_name"
        result = db.session.execute(sql, {"community_name": community_name, "user_id": user_id})
        return result.fetchone()

    def join_community(self, community_id, user_id):
        sql = "INSERT INTO community_users (community_id, user_id) VALUES (:community_id, :user_id)"
        db.session.execute(sql, {"community_id": community_id, "user_id": user_id})
        db.session.commit()

    def add_admin(self, community_id, user_id):
        sql = "UPDATE community_users SET admin=TRUE WHERE community_users.community_id=:community_id AND community_users.user_id = :user_id"
        db.session.execute(sql, {"community_id": community_id, "user_id": user_id})
        db.session.commit()

    def ban(self, community_id, user_id):
        sql = "UPDATE community_users SET banned=TRUE, admin=FALSE WHERE community_users.community_id=:community_id AND community_users.user_id = :user_id"
        db.session.execute(sql, {"community_id": community_id, "user_id": user_id})
        db.session.commit()


    def get_users(self, community_name):
        sql = "SELECT * from communities INNER JOIN community_users ON community_users.community_id = communities.id INNER JOIN users ON community_users.user_id = users.id WHERE communities.name = :community_name"
        result = db.session.execute(sql, {"community_name": community_name})
        return result.fetchall()

    def leave(self, community_id, user_id):
        sql = "DELETE from community_users WHERE community_id=:community_id AND user_id=:user_id AND banned=FALSE"
        db.session.execute(sql, {"community_id" : community_id, "user_id": user_id})
        db.session.commit()

    
communities_repository = CommunitiesRepository()