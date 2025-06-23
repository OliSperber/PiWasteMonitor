import cv2
from ultralytics import YOLO
from datetime import datetime

class YoloV8:
    def __init__(self, model_path):
        self.model = YOLO(model_path) 

    def analyze_image(self, image_path, min_confidence=0.4):
        results = self.model(image_path)
        detections = []
        for result in results:
            for det in result.boxes.data.cpu().numpy():
                confidence = float(det[4])
                if confidence < min_confidence:
                    continue
                class_id = int(det[5])
                class_name = self.model.names[class_id]
                # Bounding box coords: [x1, y1, x2, y2]
                bbox = det[:4].astype(int)
                detections.append({
                    "class": class_name,
                    "confidence": confidence,
                    "bbox": bbox
                })

        self.save_annotated_image("capture.jpg", detections, "output_annotated.jpg")
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

    def save_annotated_image(self, image_path, detections, output_path):
        img = cv2.imread(image_path)
        if img is None:
            print(f"Kan afbeelding niet laden: {image_path}")
            return False

        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            label = f"{det['class']} {det['confidence']:.2f}"

            # Tekenen van rechthoek (bbox)
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Tekst achtergrond
            (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
            cv2.rectangle(img, (x1, y1 - 20), (x1 + w, y1), (0, 255, 0), -1)

            # Tekst zelf
            cv2.putText(img, label, (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)

        # Opslaan
        cv2.imwrite(output_path, img)
        return True
