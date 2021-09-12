from flask import flash
from services.users import (users_service as default_users_service)

class ValidationService:
    def __init__(self, users_service=default_users_service):

        self._users_service = users_service
        self._limit_text = 100
        self._limit_textarea = 5000
        self._limit_password = 8

    def validate_thread(self, title, content):

        if len(title) == 0:
            flash("Otsikko ei saa olla tyhjä", "warning")
            return False

        if len(title) > self._limit_text:
            flash("Otsikko on liian pitkä", "warning")
            return False

        if len(content) == 0:
            flash("Sisältö ei saa olla tyhjä", "warning")
            return False

        if len(content) > self._limit_textarea:
            flash("Sisältö on liian pitkä", "warning")
            return False

        return True

    def validate_message(self, content):
        if len(content) == 0:
            flash("Kommentti on tyhjä", "warning")
            return False

        if len(content) > self._limit_textarea:
            flash("Kommentti on liian pitkä", "warning")
            return False

        return True

    def validate_user(self, username, password):

        if len(username) == 0:
            flash("Käyttäjätunnus ei saa olla tyhjä", "warning")
            return False

        if len(username) > self._limit_text:
            flash("Käyttäjätunnus on liian pitkä", "warning")
            return False

        if len(password) < self._limit_password:
            flash("Salasana on liian lyhyt", "warning")
            return False

        if len(password) > self._limit_text:
            flash("Salasana on liian pitkä", "warning")
            return False

        if self._users_service.username_taken(username):
            flash("Käyttäjänimi on jo otettu", "warning")
            return False
        
        return True

    def validate_community(self, name, description):

        if len(name) == 0:
            flash("Nimi ei saa olla tyhjä", "warning")
            return False

        if len(name) > self._limit_text:
            flash("Nimi on liian pitkä", "warning")
            return False

        if len(description) == 0:
            flash("Kuvaus ei saa olla tyhjä", "warning")
            return False

        if len(description) > self._limit_textarea:
            flash("Kuvaus on liian pitkä", "warning")
            return False

        return True
        

validation_service = ValidationService()