from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from services.users import users_service
from services.communities import communities_service
from services.threads import threads_service
from app import app
from db import db


@app.route("/")
def index():
    if session:
        if session["username"]:
            return redirect("/homepage")
    return render_template("index.html")

@app.route("/homepage")
def homepage():
    communities_user_not_in = communities_service.get_communities_user_not_in(session["username"])
    communities_user_in = communities_service.get_communities_user_in(session["username"])
    return render_template("homepage.html", communities_user_not_in=communities_user_not_in, communities_user_in=communities_user_in)

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if users_service.login(username, password):
        session["username"] = username
    
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        users_service.create_user(username, password)
        return redirect("/")

@app.route("/create_community", methods=["GET", "POST"])
def create_community():
    if request.method == "GET":
        return render_template("create_community.html")
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        communities_service.create_community(name, description, session["username"])
        return redirect("/")

@app.route("/community/<community_name>")
def community(community_name):
    community = communities_service.get_community(community_name)
    user_in = community in communities_service.get_communities_user_not_in(session["username"])
    threads = communities_service.get_threads(community_name)
    return render_template("community.html", community=community, user_in =user_in, threads=threads)

@app.route("/join/<community_name>")
def join(community_name):
    communities_service.join_community(community_name, session["username"])
    return redirect("/")

@app.route("/create_a_thread", methods=["GET", "POST"])
def create_a_thread():
    if request.method == "GET":
        communities = communities_service.get_communities_user_in(session["username"])
        return render_template("create_a_thread.html", communities=communities)
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        community_name = request.form["community_name"]
        threads_service.create_a_thread(community_name,title, content)
        return redirect("/")

