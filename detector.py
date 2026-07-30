from ultralytics import YOLO
import cv2


class ObjectDetector:
    """
    Object Detection using YOLOv8
    """

    def __init__(self, model_path="yolov8n.pt", confidence=0.5):

        # Load YOLO model
        self.model = YOLO(model_path)

        # Minimum confidence required
        self.confidence = confidence

        # COCO class names
        self.class_names = self.model.names

        # Classes we actually care about
        self.allowed_classes = {
            "person",
            "car",
            "bus",
            "truck",
            "motorcycle",
            "bicycle"
        }

    def detect(self, frame):
        """
        Detect objects in a frame.
        Returns:
            detections -> list of dictionaries
            annotated_frame -> frame with bounding boxes
        """

        results = self.model(frame, verbose=False)

        detections = []

        annotated_frame = frame.copy()

        for result in results:

            boxes = result.boxes

            for box in boxes:

                confidence = float(box.conf[0])

                if confidence < self.confidence:
                    continue

                class_id = int(box.cls[0])

                class_name = self.class_names[class_id]

                if class_name not in self.allowed_classes:
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                detections.append({

                    "class": class_name,
                    "confidence": confidence,
                    "bbox": (x1, y1, x2, y2)

                })

                label = f"{class_name} {confidence:.2f}"

                cv2.rectangle(
                    annotated_frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    annotated_frame,
                    label,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )

        return detections, annotated_frame