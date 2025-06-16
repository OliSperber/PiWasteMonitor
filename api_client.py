import requests
import json

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')

    def send_results(self, objects_bulk):
        url = f"{self.base_url}/api/wastedetection/bulk"
        try:
            response = requests.post(url, json=objects_bulk, timeout=10)
            print(f"Status code: {response.status_code}")
            print("Response body:", response.text)
            if response.status_code == 401:
                print("401 Unauthorized - verwijder detectie lokaal")
                return 401
            response.raise_for_status()
            print("Data succesvol verzonden")
            return response.status_code
        except requests.RequestException as e:
            print(f"Fout bij verzenden: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Status code: {e.response.status_code}")
                print("Response body:", e.response.text)
            return None

    def is_online(self):
        url = f"{self.base_url}/api"
        try:
            response = requests.get(url, timeout=5)
            print(f"Status code: {response.status_code}")
            print("Response body:", response.text)
            response.raise_for_status()
            json_data = response.json()
            return json_data.get("status") == "online"
        except requests.RequestException as e:
            print(f"Fout bij controleren API: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Status code: {e.response.status_code}")
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