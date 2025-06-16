import requests
import json

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')

    def send_results(self, objects_bulk):
        url = f"{self.base_url}/api/wastedetection/bulk"
        try:
            response = requests.post(url, json=objects_bulk, timeout=10)
            try:
                print("Response:", json.dumps(response.json(), indent=2))
            except Exception:
                print("Response (geen JSON):", response.text)
            if response.status_code == 401:
                print("401 Unauthorized - verwijder detectie lokaal")
                return 401
            response.raise_for_status()
            print("Data succesvol verzonden")
            return response.status_code
        except requests.RequestException as e:
            print(f"Fout bij verzenden: {e}")
            return None

    def is_online(self):
        url = f"{self.base_url}/api"
        try:
            response = requests.get(url, timeout=5)
            try:
                print("Response:", json.dumps(response.json(), indent=2))
            except Exception:
                print("Response (geen JSON):", response.text)
            response.raise_for_status()
            json_data = response.json()
            return json_data.get("status") == "online"
        except requests.RequestException:
            return False

    def has_internet_connection(self):
        try:
            response = requests.get("http://google.com", timeout=3)
            print("Response:", response.text)
            return True
        except requests.RequestException:
            return False