import time
import socket
from datetime import datetime, timedelta
from camera_oakd import CameraOakD
from yolo_v8 import YoloV8
from api_client import APIClient
from object_manager import ObjectManager
from geo_coder import GeoCoder

def wait_until_next_half_hour():
    now = datetime.now()
    minute = now.minute
    second = now.second
    microsecond = now.microsecond

    if minute < 30:
        next_time = now.replace(minute=30, second=0, microsecond=0)
    else:
        next_time = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)

    wait_seconds = (next_time - now).total_seconds()
    print(f"Wachten tot {next_time.strftime('%H:%M:%S')} ({int(wait_seconds)} seconden)")
    time.sleep(wait_seconds)

def main():
    camera_id = socket.gethostname()
    model_path = "path_to_your_trained_model.pt"
    api_url = "https://jouw-api-url"

    camera = CameraOakD()
    detector = YoloV8(model_path)
    api = APIClient(api_url)
    store = ObjectManager()
    gps = GeoCoder()

    print(gps.get_coords())

    while True:
        # Oude detecties versturen
        pending = store.load_all()
        if pending and api.is_online():
            print(f"Verstuur {len(pending)} oude detecties")
            for detection in pending:
                status = api.send_results(detection)
                if status == 401:
                    store.remove_detection(detection)
                elif status is None:
                    print("Kan detectie nog niet versturen, probeer later")
                else:
                    store.remove_detection(detection)

        # Nieuwe detectie
        image_path = camera.capture_image()
        if image_path:
            objects = detector.analyze_image(image_path)
            if objects:
                lat, lon = gps.get_coords()
                bulk_data = detector.create_detection_object(camera_id, objects, lat, lon)
                print(f"Nieuwe detectie bulk: {bulk_data}")
                if isinstance(bulk_data, list):
                    store.add_detections(bulk_data)
                else:
                    store.add_detection(bulk_data)
            else:
                print("Geen objecten gevonden")
        else:
            print("Foto maken mislukt")

        wait_until_next_half_hour()

if __name__ == "__main__":
    main()