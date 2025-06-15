import time
from camera_oakd import CameraOakD
from yolo_v8 import YoloV8
from api_client import APIClient
from object_manager import ObjectManager
from gps_navilock import GPSNaviLock

def main():
    camera_id = "CAM01"
    model_path = "path_to_your_trained_model.pt"
    api_url = "https://jouw-api-url"

    camera = CameraOakD()
    detector = YoloV8(model_path)
    api = APIClient(api_url)
    store = ObjectManager()
    gps = GPSNaviLock()

    if not api.is_online():
        print("API offline, stop")
        return

    while True:
        # Eerst oude detecties versturen
        pending = store.load_all()
        if pending:
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
                store.add_detection(bulk_data)
            else:
                print("Geen objecten gevonden")
        else:
            print("Foto maken mislukt")

        print("Wachten 30 minuten...")
        time.sleep(1800)

if __name__ == "__main__":
    main()
