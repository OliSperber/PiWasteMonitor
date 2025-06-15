import json
import os

class ObjectManager:
    def __init__(self, filename="detections.json"):
        self.filename = filename
        if not os.path.isfile(self.filename):
            with open(self.filename, 'w') as f:
                json.dump([], f)

    def load_all(self):
        with open(self.filename, 'r') as f:
            return json.load(f)

    def save_all(self, detections):
        with open(self.filename, 'w') as f:
            json.dump(detections, f, indent=2)

    def add_detection(self, detection):
        detections = self.load_all()
        detections.append(detection)
        self.save_all(detections)

    def remove_detection(self, detection):
        detections = self.load_all()
        detections = [d for d in detections if d != detection]
        self.save_all(detections)
