import depthai as dai
import time

class CameraOakD:
    def __init__(self):
        self.pipeline = dai.Pipeline()
        cam = self.pipeline.createColorCamera()
        cam.setPreviewSize(640, 480)
        cam.setInterleaved(False)
        self.xout = self.pipeline.createXLinkOut()
        self.xout.setStreamName("preview")
        cam.preview.link(self.xout.input)
        self.device = dai.Device(self.pipeline)
        self.q = self.device.getOutputQueue(name="preview", maxSize=4, blocking=False)

    def capture_image(self, save_path="capture.jpg"):
        frame = None
        for _ in range(30):  # wacht max ~1 sec op frame
            in_frame = self.q.tryGet()
            if in_frame is not None:
                frame = in_frame.getCvFrame()
                break
            time.sleep(0.03)
        if frame is not None:
            import cv2
            cv2.imwrite(save_path, frame)
            return save_path
        else:
            print("Geen frame ontvangen")
            return None
