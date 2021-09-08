from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from services.users import users_service
from app import app
from db import db


@app.route("/")
def index():
    return render_template("index.html")

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
        communities_service.create_community(name)

