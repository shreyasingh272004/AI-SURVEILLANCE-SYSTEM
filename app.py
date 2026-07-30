import cv2
import numpy as np
from tracker import ObjectTracker
from zone_detection import RestrictedZone
from logger import EventLogger
from threat_engine import ThreatEngine
from ui import UIManager
from loitering import LoiteringDetector
from crowd_detection import CrowdDetector
from screenshot import ScreenshotManager

def main():

    # Initialize modules
    tracker = ObjectTracker()
    zone = RestrictedZone()
    logger = EventLogger()
    threat_engine = ThreatEngine()
    loitering_detector = LoiteringDetector()
    crowd_detector = CrowdDetector()
    screenshot_manager = ScreenshotManager()


    # Store IDs already logged while inside the zone
    logged_intrusions = set()
    logged_crowd = False
    crowd_detected_last_frame = False
    current_intrusions = set()
    logged_loitering = set()
    current_loitering = set()

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Cannot open camera.")
        return

    print("Press 'q' to quit.")

    while True:

        success, frame = cap.read()

        if not success:
            break
        # Create heatmap using the camera's actual resolution
        if 'heatmap' not in locals():
            heatmap = np.zeros(frame.shape[:2], dtype=np.float32)

        if not success:
            break

        # Track objects
        results = tracker.track(frame)

        annotated_frame = frame.copy()
        person_count = 0

        # Draw restricted zone
        UIManager.draw_zone(annotated_frame, zone)

        # IDs currently inside the zone in THIS frame
        current_intrusions.clear()
        current_loitering.clear()

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

                # -----------------------------
                # Update Heatmap
                # -----------------------------
                if class_name == "person":
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    cv2.circle(
                        heatmap,
                        (center_x, center_y),
                        50,
                        10,
                        -1
                    )

                label = f"{class_name} #{track_id} ({confidence:.2f})"

                intrusion = False

                # Check intrusion only for persons
                if class_name == "person":
                    intrusion = zone.is_inside(bbox)
                    loitering = False
                    if class_name == "person":
                        loitering = loitering_detector.update(
                            track_id,
                            intrusion
                        )

                # -----------------------------
                # Intrusion
                # -----------------------------
                if intrusion:

                    current_intrusions.add(track_id)

                    color = (0, 0, 255)
                    label = f"INTRUSION! {class_name} #{track_id}"

                    if track_id not in logged_intrusions:

                        threat = threat_engine.evaluate(
                            event_type="Intrusion",
                            class_name=class_name
                        )

                        logger.log_event(
                            event_type="Intrusion",
                            track_id=track_id,
                            class_name=class_name,
                            threat_level=threat
                        )
                        screenshot_manager.save(
                            annotated_frame,
                            "intrusion"
                        )

                        logged_intrusions.add(track_id)

                    UIManager.draw_alert(
                        annotated_frame,
                        "INTRUSION ALERT!",
                        y=40
                    )
                    if loitering:
                        current_loitering.add(track_id)
                        if track_id not in logged_loitering:
                            threat = threat_engine.evaluate(
                                  event_type="Loitering",
                                  class_name=class_name
                            )
                            logger.log_event(
                                event_type="Loitering",
                                track_id=track_id,
                                class_name=class_name,
                                threat_level=threat
                            )
                            screenshot_manager.save(
                                annotated_frame,
                                "loitering"
                            )
                            logged_loitering.add(track_id)
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
        logged_intrusions.intersection_update(current_intrusions)
        logged_loitering.intersection_update(current_loitering)


        # Crowd Detection
        crowd_detected = crowd_detector.detect(person_count)
        if crowd_detected:
            UIManager.draw_crowd_alert(annotated_frame)
            if not logged_crowd:
                threat = threat_engine.evaluate(
                    event_type="Crowd",
                    class_name="person"
                )
                logger.log_event(
                    event_type="Crowd",
                    track_id=0,
                    class_name="person",
                    threat_level=threat
                )
                screenshot_manager.save(
                    annotated_frame,
                    "crowd"
                )
                logged_crowd = True
        else:
            logged_crowd = False
        # Show output
        cv2.imshow(
            "AI Threat Detection System",
            annotated_frame
        )

        # -----------------------------
        # Display Heatmap
        # -----------------------------
        # Gradually fade old detections
        # 
        heatmap *= 0.995

        # Normalize heatmap values
        heatmap_normalized = cv2.normalize(
            heatmap,
            None,
            0,
            255,
            cv2.NORM_MINMAX
        ).astype(np.uint8)

        # Apply color map
        heatmap_colored = cv2.applyColorMap(
            heatmap_normalized,
            cv2.COLORMAP_JET
        )

        # Blend with camera frame
        annotated_frame = cv2.addWeighted(
            annotated_frame,
            0.55,
            heatmap_colored,
            0.45,
            0
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q") or key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()