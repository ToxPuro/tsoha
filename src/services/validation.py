class ValidationService:
    def __init__(self):

        self._limit_text = 100
        self._limit_textarea = 5000
        self._limit_password = 8

    def validate_thread(self, title, content):

        error_message = ""
        passed = True
        if len(title) == 0:
            error_message = "Otsikko ei saa olla tyhjä"
            passed = False

        if len(title) > self._limit_text:
            error_message = "Otsikko on liian pitkä"
            passed = False

        if len(content) == 0:
            error_message = "Sisältö ei saa olla tyhjä"
            passed = False

        if len(content) > self._limit_textarea:
            error_message = "Sisältö on liian pitkä"
            passed = False

        return {"error_message":error_message, "passed":passed}

    def validate_message(self, content):
        passed = True
        error_message=""
        if len(content) == 0:
            error_message = "Kommentti on tyhjä"
            passed = False

        if len(content) > self._limit_textarea:
            error_message = "Kommentti on liian pitkä"
            passed = False

        return {"error_message":error_message, "passed":passed}

    def validate_user(self, username, password):
        passed = True
        error_message = ""

        if len(username) == 0:
            error_message = "Käyttäjätunnus ei saa olla tyhjä"
            passed = False

        if len(username) > self._limit_text:
            error_message = "Käyttäjätunnus on liian pitkä"
            passed = False

        if len(password) < self._limit_password:
            error_message = "Salasana on liian lyhyt"
            passed = False

        if len(password) > self._limit_text:
            error_message = "Salasana on liian pitkä"
            passed = False
        
        return {"error_message":error_message, "passed":passed}

    def validate_community(self, name, description):
        passed = True
        error_message = ""

        if len(name) == 0:
            error_message = "Nimi ei saa olla tyhjä"
            passed = False

        if len(name) > self._limit_text:
            error_message = "Nimi on liian pitkä"
            passed = False

        if len(description) == 0:
            error_message = "Kuvaus ei saa olla tyhjä"
            passed = False

        if len(description) > self._limit_textarea:
            error_message = "Kuvaus on liian pitkä"
            passed = False

        return {"error_message":error_message, "passed":passed}
        

validation_service = ValidationService()