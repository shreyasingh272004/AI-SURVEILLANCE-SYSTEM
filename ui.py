import cv2


class UIManager:
    """
    Handles all drawing operations.
    """

    @staticmethod
    def draw_zone(frame, zone):

        x1, y1, x2, y2 = zone.get_coordinates()

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 0, 255),
            2
        )

        cv2.putText(
            frame,
            "RESTRICTED ZONE",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

    @staticmethod
    def draw_detection(frame, bbox, label, color):

        x1, y1, x2, y2 = bbox

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            color,
            2
        )

        cv2.putText(
            frame,
            label,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )

    @staticmethod
    def draw_alert(frame, text,y=40):

        cv2.putText(
            frame,
            text,
            (20, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

    @staticmethod
    def draw_crowd_alert(frame):

        cv2.putText(
            frame,
            "CROWD DETECTED!",
            (20, 130),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )