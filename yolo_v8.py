from ultralytics import YOLO
from datetime import datetime

class YoloV8:
    def __init__(self, model_path):
        #self.model = YOLO(model_path)
        self.model = YOLO('yolov8n.pt') # For testing

    def analyze_image(self, image_path):
        results = self.model(image_path)
        detections = []
        for result in results:
            for det in result.boxes.data.cpu().numpy():
                # [x1, y1, x2, y2, confidence, class]
                confidence = float(det[4])
                class_id = int(det[5])
                class_name = self.model.names[class_id]
                detections.append({"class": class_name, "confidence": confidence})
        return detections

    def create_detection_object(self, camera_id, detected_objects, latitude, longitude):
        now = datetime.utcnow().isoformat() + "Z"
        bulk_data = []
        for obj in detected_objects:
            bulk_data.append({
                "cameraId": camera_id,
                "confidence": f"{obj['confidence']:.2f}",
                "dateTime": now,
                "location": {
                    "latitude": str(latitude),
                    "longitude": str(longitude)
                },
                "type": obj["class"]
            })
        return bulk_data
