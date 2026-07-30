import cv2

from tracker import ObjectTracker
from zone_detection import RestrictedZone
from logger import EventLogger
from threat_engine import ThreatEngine
from ui import UIManager
from loitering import LoiteringDetector
from crowd_detection import CrowdDetector
from screenshot import ScreenshotManager


class AIEngine:

    def __init__(self):

        self.tracker = ObjectTracker()
        self.zone = RestrictedZone()
        self.logger = EventLogger()
        self.threat_engine = ThreatEngine()
        self.loitering_detector = LoiteringDetector()
        self.crowd_detector = CrowdDetector()
        self.screenshot_manager = ScreenshotManager()

        self.logged_intrusions = set()
        self.logged_loitering = set()

        self.current_intrusions = set()
        self.current_loitering = set()

        self.logged_crowd = False

    def process_frame(self, frame):
        results = self.tracker.track(frame)
        annotated_frame = frame.copy()
        person_count = 0
        UIManager.draw_zone(
            annotated_frame,
            self.zone
        )
        self.current_intrusions.clear()
        self.current_loitering.clear()

        # Process detections
        for result in results:
            if result.boxes is None:
                continue
            for box in result.boxes:
                        # Skip detections without tracking IDs
                if box.id is None:
                    continue
        
                track_id = int(box.id[0])
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
        
                class_name = result.names[class_id]
                if class_name == "person":
                    person_count += 1
        
                x1, y1, x2, y2 = map(int, box.xyxy[0])
        
                bbox = (x1, y1, x2, y2)
        
                label = f"{class_name} #{track_id} ({confidence:.2f})"
        
                intrusion = False
        
                # Check intrusion only for persons
                if class_name == "person":
                    intrusion = self.zone.is_inside(bbox)
                    loitering = False
                    if class_name == "person":
                        loitering = self.loitering_detector.update(
                            track_id,
                            intrusion
                        )
        
                # -----------------------------
                # Intrusion
                # -----------------------------
                if intrusion:
        
                    self.current_intrusions.add(track_id)
        
                    color = (0, 0, 255)
                    label = f"INTRUSION! {class_name} #{track_id}"
        
                    if track_id not in self.logged_intrusions:
        
                        threat = self.threat_engine.evaluate(
                            event_type="Intrusion",
                            class_name=class_name
                        )
        
                        self.logger.log_event(
                            event_type="Intrusion",
                            track_id=track_id,
                            class_name=class_name,
                            threat_level=threat
                        )
                        self.screenshot_manager.save(
                            annotated_frame,
                            "intrusion"
                        )
        
                        self.logged_intrusions.add(track_id)
        
                    UIManager.draw_alert(
                        annotated_frame,
                         "INTRUSION ALERT!",
                        y=40
                    )
                    if loitering:
                        self.current_loitering.add(track_id)
                        if track_id not in self.logged_loitering:
                            threat = self.threat_engine.evaluate(
                                event_type="Loitering",
                                class_name=class_name
                            )
                            self.logger.log_event(
                                event_type="Loitering",
                                track_id=track_id,
                                class_name=class_name,
                                threat_level=threat
                            )
                            self.screenshot_manager.save(
                                annotated_frame,
                                "loitering"
                            )
                            self.logged_loitering.add(track_id)
                        UIManager.draw_alert(
                            annotated_frame,
                            "LOITERING DETECTED!",
                            y=85
                        )
                            
        
                else:
                    color = (255, 0, 0)
        
                # Draw bounding box
                UIManager.draw_detection(
                    annotated_frame,
                    bbox,
                    label,
                    color
                )
        
        # Remove IDs that have left the zone
        self.logged_intrusions.intersection_update(self.current_intrusions)
        self.logged_loitering.intersection_update(self.current_loitering)
        
        
        # Crowd Detection
        crowd_detected = self.crowd_detector.detect(person_count)
        if crowd_detected:
            UIManager.draw_crowd_alert(annotated_frame)
            if not self.logged_crowd:
                threat = self.threat_engine.evaluate(
                    event_type="Crowd",
                    class_name="person"
                )
                self.logger.log_event(
                    event_type="Crowd",
                    track_id=0,
                    class_name="person",
                    threat_level=threat
                )
                self.screenshot_manager.save(
                    annotated_frame,
                    "crowd"
                )
                self.logged_crowd = True
        else:
            self.logged_crowd = False
        return annotated_frame


