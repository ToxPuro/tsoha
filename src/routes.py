from flask import Flask
from flask import redirect, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from services.users import users_service
from services.communities import communities_service
from services.threads import threads_service
from services.messages import messages_service
from services.validation import validation_service
from app import app
from db import db

def flash_error(error):
    error = error.args[0] if len(error.args) > 0 else None
    category = "warning"
    if error is None:
        error = "Not authorized"
        category = "danger"
    flash(error, category)


@app.route("/")
def index():
    if not session:
        return render_template("index.html")

    if not "username" in session.keys():
        return render_template("index.html")
            
    return redirect("/homepage")

@app.route("/homepage")
def homepage():

    if not session:
        return redirect("/")

    if not "username" in session.keys():
        return redirect("/")

    communities = communities_service.get_communities(session["username"])
    threads = users_service.get_threads(session["username"])
    return render_template("homepage.html", threads=threads, communities=communities)

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if users_service.login(username, password):
        session["username"] = username

    else:
        flash("Kirjautuminen ei onnistunut", "warning")
    
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

        input_validation = validation_service.validate_user(username, password)
        if not input_validation["passed"]:
            flash(input_validation["error_message"], "warning")
            return redirect("/register")

        if users_service.username_taken(username):
            flash("Käyttäjänimi on jo otettu", "warning")
            return redirect("/register")

        session["username"] = username
        users_service.create_user(username, password)
        flash("Rekisteröity", "success")
        return redirect("/")

@app.route("/create_community", methods=["GET", "POST"])
def create_community():

    if not session:
        return redirect("/")

    if not "username" in session.keys():
        return redirect("/")

    if request.method == "GET":
        return render_template("create_community.html")
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]

        input_validation = validation_service.validate_community(name, description)
        if not input_validation["passed"]:
            flash(input_validation["error_message"], "warning")
            return redirect("/create_community")
        
        communities_service.create_community(name, description, session["username"])
        return redirect("/")

@app.route("/community/<community_name>")
def community(community_name):

    if not session:
        return redirect("/")

    if not "username" in session.keys():
        return redirect("/")

    community = communities_service.get_community(community_name, session["username"])

    if community.user_banned:
        flash(f"Olet estetty ryhmästä {community_name}", "warning")
        return redirect("/")

    threads = communities_service.get_threads(community_name)
    users = communities_service.get_users(community_name)
    return render_template("community.html", community=community, threads=threads, users=users)

@app.route("/join/<community_name>")
def join(community_name):
    if not session:
        return redirect("/")

    if not "username" in session.keys():
        return redirect("/")

    community = communities_service.get_community(community_name, session["username"])
    if community.user_banned:
        flash(f"Olet estetty ryhmästä {community_name}", "warning")
        return redirect("/")

    communities_service.join_community(community_name, session["username"])
    return redirect("/")

@app.route("/create_a_thread", methods=["GET", "POST"])
def create_a_thread():

    if not session:
        return redirect("/")

    if not "username" in session.keys():
        return redirect("/")

    if request.method == "GET":
        communities = communities_service.get_communities(session["username"])
        return render_template("create_a_thread.html", communities=communities)
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        community_name = request.form["community_name"]

        input_validation = validation_service.validate_thread(title, content)

        if not input_validation["passed"]:
            flash(input_validation["error_message"], "warning")
            return redirect("/create_a_thread")

        community = communities_service.get_community(community_name, session["username"])
        if community.user_banned:
            flash(f"Olet estetty ryhmästä {community_name}", "warning")
            return redirect("/")

        threads_service.create_a_thread(community_name, session["username"], title, content)
        flash("Ketju luotu", "success")
        return redirect("/")

@app.route("/thread/<int:thread_id>", methods=["GET", "POST"])
def thread(thread_id):

    if not session:
        return redirect("/")

    if not "username" in session.keys():
        return redirect("/")

    thread = threads_service.get_thread(thread_id, session["username"])
    if thread.user_is_banned:
        flash("Olet estetty ketjun ryhmästä", "warning")
        return redirect("/")

    messages = threads_service.get_messages(thread_id, session["username"])
    return render_template("thread.html", thread=thread, messages=messages)

@app.route("/message/<int:thread_id>", methods=["POST"])
def message(thread_id):

    if not session:
        return redirect("/")

    if not "username" in session.keys():
        return redirect("/")

    content = request.form["content"]

    input_validation = validation_service.validate_message(content)

    thread = threads_service.get_thread(thread_id, session["username"])
    if thread.user_is_banned:
        flash("Olet estetty ketjun ryhmästä", "warning")
        return redirect("/")

    if not input_validation["passed"]:
        flash(input_validation["error_message"], "warning")
        return redirect(f"/thread/{thread_id}")

    user = users_service.get_user_by_name(session["username"])
    threads_service.add_message(thread_id, user.id, content)
    return redirect(f"/thread/{thread_id}")

@app.route("/upvote/<int:thread_id>", methods=["POST"])
def upvote(thread_id):

    if not session:
        return redirect("/")

    if not "username" in session.keys():
        return redirect("/")

    user = users_service.get_user_by_name(session["username"])

    thread = threads_service.get_thread(thread_id, session["username"])
    if thread.user_is_banned:
        flash("Olet estetty ketjun ryhmästä", "warning")
        return redirect("/")

    threads_service.upvote(thread_id, user.id)
    flash("Äänestetty", "success")
    return redirect(f"/thread/{thread_id}")

@app.route("/downvote/<int:thread_id>", methods=["POST"])
def downvote(thread_id):
    if not session:
        return redirect("/")

    if not "username" in session.keys():
        return redirect("/")

    user = users_service.get_user_by_name(session["username"])

    thread = threads_service.get_thread(thread_id, session["username"])
    if thread.user_is_banned:
        flash("Olet estetty ketjun ryhmästä", "warning")
        return redirect("/")

    threads_service.downvote(thread_id, user.id)
    flash("Äänestetty", "success")
    return redirect(f"/thread/{thread_id}")

@app.route("/upvote/message/<int:thread_id>/<int:message_id>", methods=["POST"])
def upvote_message(thread_id, message_id):
    if not session:
        return redirect("/")

    if not "username" in session.keys():
        return redirect("/")

    thread = threads_service.get_thread(thread_id, session["username"])
    if thread.user_is_banned:
        flash("Olet estetty ketjun ryhmästä", "warning")
        return redirect("/")

    user = users_service.get_user_by_name(session["username"])
    messages_service.upvote(message_id, user.id)
    flash("Äänestetty", "success")
    return redirect(f"/thread/{thread_id}")

@app.route("/downvote/message/<int:thread_id>/<int:message_id>", methods=["POST"])
def downvote_message(thread_id, message_id):
    if not session:
        return redirect("/")

    if not "username" in session.keys():
        return redirect("/")

    thread = threads_service.get_thread(thread_id, session["username"])
    if thread.user_is_banned:
        flash("Olet estetty ketjun ryhmästä", "warning")
        return redirect("/")

    user = users_service.get_user_by_name(session["username"])
    messages_service.downvote(message_id, user.id)
    flash("Äänestetty", "success")
    return redirect(f"/thread/{thread_id}")

@app.route("/delete/thread/<int:thread_id>", methods=["POST"])
def delete_thread(thread_id):

    if not session:
        return redirect("/")

    if not "username" in session.keys():
        return redirect("/")

    thread = threads_service.get_thread(thread_id, session["username"])
    if not thread.is_users and not thread.user_is_admin:
        flash("Sinulla ei ole oikeutta poistaa ketjua", "warning")
        return redirect("/")

    threads_service.delete_thread(thread_id)
    flash("Ketju poistettu", "success")
    return redirect("/")

@app.route("/delete/message/<int:thread_id>/<int:message_id>", methods=["POST"])
def delete_message(thread_id, message_id):

    if not session:
        return redirect("/")

    if not "username" in session.keys():
        return redirect("/")

    thread = threads_service.get_thread(thread_id, session["username"])
    message = messages_service.get_message(message_id, session["username"])
    if not message.is_users and not thread.user_is_admin:
        flash("Sinulla ei ole oikeutta poistaa viestiä", "warning")
        return redirect("/")

    messages_service.delete(message_id)
    flash("Viesti poistettu", "success")
    return redirect(f"/thread/{thread_id}")

@app.route("/edit/thread/<int:thread_id>", methods=["GET", "POST"])
def edit_thread(thread_id):

    if not session:
        return redirect("/")

    if not "username" in session.keys():
        return redirect("/")

    if request.method == "GET":
        thread = threads_service.get_thread(thread_id, session["username"])
        return render_template("edit_thread.html", thread=thread)

    if request.method == "POST":
        new_title = request.form["title"]
        new_content = request.form["content"]

        thread = threads_service.get_thread(thread_id, session["username"])
        if not thread.is_users and not thread.user_is_admin:
            flash("Sinulla ei ole oikeutta muokata ketjua", "warning")
            return redirect("/")

        input_validation = validation_service.validate_thread(title, content)

        if not input_validation["passed"]:
            flash(input_validation["error_message"], "warning")
            return redirect(f"/edit/thread/{thread_id}")
    
        threads_service.edit_thread(thread_id, new_title, new_content)
        flash("Muokattu", "success")
        return redirect(f"/thread/{thread_id}")

@app.route("/edit/message/<int:thread_id>/<int:message_id>", methods=["GET", "POST"])
def edit_message(thread_id, message_id):

    if not session:
        return redirect("/")

    if not "username" in session.keys():
        return redirect("/")

    if request.method == "GET":
        message = messages_service.get_message(message_id)
        return render_template("edit_message.html", message=message, thread_id=thread_id)

    if request.method == "POST":
        new_content = request.form["content"]

        thread = threads_service.get_thread(thread_id, session["username"])
        message = messages_service.get_message(message_id, session["username"])
        if not message.is_users and not thread.user_is_admin:
            flash("Sinulla ei ole oikeutta muokata viestiä", "warning")
            return redirect("/")

        input_validation = validation_service.validate_message(content)
        if not input_validation["passed"]:
            flash(input_validation["error_message"], "warning")
            return redirect(f"/edit/message/{thread_id}/{message_id}")

        messages_service.edit(message_id, new_content)
        flash("Muokattu", "success")
        return redirect(f"/thread/{thread_id}")

@app.route("/admin/<community_name>/<username>")
def admin(community_name, username):

    if not session:
        return redirect("/")

    if not "username" in session.keys():
        return redirect("/")

    community = communities_service.get_community(community_name, session["username"])
    if not community.user_is_admin:
        flash(f"Sinun täytyy olla ryhmän {community_name} ylläpitäjä")
        redirect("/community/{community_name}")

    communities_service.add_admin(community_name, username)
    flash("Lisätty ylläpitäjä", "success")
    return redirect(f"/community/{community_name}")

@app.route("/ban/<community_name>/<username>")
def ban(community_name, username):

    if not session:
        return redirect("/")

    if not "username" in session.keys():
        return redirect("/")

    community = communities_service.get_community(community_name, session["username"])
    if not community.user_is_admin:
        flash(f"Sinun täytyy olla ryhmän {community_name} ylläpitäjä")
        redirect("/community/{community_name}")

    communities_service.ban(community_name, username)
    flash("Estetty käyttäjä", "success")
    return redirect(f"/community/{community_name}")

@app.route("/leave/<community_name>")
def leave(community_name):

    if not session:
        return redirect("/")

    if not "username" in session.keys():
        return redirect("/")

    community = communities_service.get_community(community_name, session["username"])
    if not community.user_is_admin:
        flash(f"Sinun täytyy olla ryhmän {community_name} ylläpitäjä")
        redirect("/community/{community_name}")

    communities_service.leave(community_name, session["username"])
    flash("Lähdetty ryhmästä", "success")
    return redirect("/")
    


