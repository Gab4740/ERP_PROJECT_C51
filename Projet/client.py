import requests

class Modele:
    def __init__(self):
        self.authenticated = False

    def verifier_identifiants(self, username, password):
        try:
            print(username, password)
            response = requests.post('http://localhost:5000/login', json={'username': username, 'password': password})
            if response.status_code == 200 and response.json().get('success'):
                self.authenticated = True
                return response.json().get('role') 
            else:
                print("erreur")
                return None
        except requests.exceptions.RequestException as e:
            print("Erreur de connexion au serveur:", e)
            return None
