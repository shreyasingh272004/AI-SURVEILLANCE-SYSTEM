from ultralytics import YOLO


class ObjectTracker:
    """
    Object Tracking using YOLOv8 built-in tracking.
    """

    def __init__(self, model_path="yolov8n.pt", confidence=0.5):

        self.model = YOLO(model_path)
        self.confidence = confidence

        self.allowed_classes = {
            "person",
            "car",
            "bus",
            "truck",
            "motorcycle",
            "bicycle"
        }

    def track(self, frame):

        results = self.model.track(
            frame,
            persist=True,
            verbose=False
        )

        return results