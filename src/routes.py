from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from services.users import users_service
from services.communities import communities_service
from services.threads import threads_service
from services.messages import messages_service
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
    communities = communities_service.get_communities(session["username"])
    threads = users_service.get_threads(session["username"])
    return render_template("homepage.html", threads=threads, communities=communities)

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
    user_in = community.name in [community.name for community in communities_service.get_communities_user_in(session["username"])]
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
        threads_service.create_a_thread(community_name, session["username"], title, content)
        return redirect("/")

@app.route("/thread/<int:thread_id>", methods=["GET", "POST"])
def thread(thread_id):
    thread = threads_service.get_thread(thread_id, session["username"])
    messages = threads_service.get_messages(thread_id, session["username"])
    return render_template("thread.html", thread=thread, messages=messages)

@app.route("/message/<int:thread_id>", methods=["POST"])
def message(thread_id):
    content = request.form["content"]
    user = users_service.get_user_by_name(session["username"])
    threads_service.add_message(thread_id, user.id, content)
    return redirect(f"/thread/{thread_id}")

@app.route("/upvote/<int:thread_id>", methods=["GET"])
def upvote(thread_id):
    user = users_service.get_user_by_name(session["username"])
    threads_service.upvote(thread_id, user.id)
    return redirect(f"/thread/{thread_id}")

@app.route("/downvote/<int:thread_id>", methods=["GET"])
def downvote(thread_id):
    user = users_service.get_user_by_name(session["username"])
    threads_service.downvote(thread_id, user.id)
    return redirect(f"/thread/{thread_id}")

@app.route("/upvote/message/<int:thread_id>/<int:message_id>", methods=["GET"])
def upvote_message(thread_id, message_id):
    user = users_service.get_user_by_name(session["username"])
    messages_service.upvote(message_id, user.id)
    return redirect(f"/thread/{thread_id}")

@app.route("/downvote/message/<int:thread_id>/<int:message_id>", methods=["GET"])
def downvote_message(thread_id, message_id):
    user = users_service.get_user_by_name(session["username"])
    messages_service.downvote(message_id, user.id)
    return redirect(f"/thread/{thread_id}")

@app.route("/delete/thread/<int:thread_id>", methods=["GET"])
def delete_thread(thread_id):
    threads_service.delete_thread(thread_id)
    return redirect("/")

@app.route("/delete/message/<int:thread_id>/<int:message_id>", methods=["GET"])
def delete_message(thread_id, message_id):
    messages_service.delete(message_id)
    return redirect(f"/thread/{thread_id}")

@app.route("/edit/thread/<int:thread_id>", methods=["GET", "POST"])
def edit_thread(thread_id):
    if request.method == "GET":
        thread = threads_service.get_thread(thread_id, session["username"])
        return render_template("edit_thread.html", thread=thread)

    if request.method == "POST":
        new_title = request.form["title"]
        new_content = request.form["content"]
        threads_service.edit_thread(thread_id, new_title, new_content)
        return redirect("/")

@app.route("/edit/message/<int:thread_id>/<int:message_id>", methods=["GET", "POST"])
def edit_message(thread_id, message_id):
    if request.method == "GET":
        message = messages_service.get_message(message_id)
        print("MESSAGE", message)
        return render_template("edit_message.html", message=message, thread_id=thread_id)

    if request.method == "POST":
        new_content = request.form["content"]
        messages_service.edit(message_id, new_content)
        return redirect(f"/thread/{thread_id}")



