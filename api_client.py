import requests
import json
import os

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.api_password = os.environ.get("API_PASSWORD")

    def send_results(self, objects_bulk):
        url = f"{self.base_url}/api/wastedetection"
        headers = {"Api-Password": self.api_password} if self.api_password else {}
        try:
            response = requests.post(url, json=objects_bulk, headers=headers, timeout=10)
            print(f"Status code: {response.status_code}")
            try:
                print("Response body:", json.dumps(response.json(), indent=2))
            except Exception:
                print("Response body:", response.text)
            if response.status_code == 201:
                print("Data succesvol aangemaakt (201)")
                return 201
            if response.status_code == 401:
                print("401 Unauthorized - verwijder detectie lokaal")
                return 401
            # Andere statuscodes worden als niet succesvol beschouwd
            return response.status_code
        except requests.RequestException as e:
            print(f"Fout bij verzenden: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Status code: {e.response.status_code}")
                try:
                    print("Response body:", json.dumps(e.response.json(), indent=2))
                except Exception:
                    print("Response body:", e.response.text)
            return None

    def is_online(self):
        url = f"{self.base_url}/api"
        headers = {"Api-Password": self.api_password} if self.api_password else {}
        try:
            response = requests.get(url, headers=headers, timeout=5)
            print(f"Status code: {response.status_code}")
            try:
                print("Response body:", json.dumps(response.json(), indent=2))
            except Exception:
                print("Response body:", response.text)
            response.raise_for_status()
            json_data = response.json()
            # Check if 'online' key exists and is True
            return json_data.get("online") is True
        except requests.RequestException as e:
            print(f"Fout bij controleren API: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Status code: {e.response.status_code}")
                try:
                    print("Response body:", json.dumps(e.response.json(), indent=2))
                except Exception:
                    print("Response body:", e.response.text)
            return False

    def has_internet_connection(self):
        try:
            response = requests.get("http://google.com", timeout=3)
            print(f"Status code: {response.status_code}")
            print("Response body:", response.text)
            return True
        except requests.RequestException as e:
            print(f"Fout bij internet check: {e}")
            return False