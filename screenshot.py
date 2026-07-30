import os
import cv2
from datetime import datetime


class ScreenshotManager:

    def __init__(self):

        self.folder = "screenshots"

        os.makedirs(self.folder, exist_ok=True)

    def save(self, frame, event_name):

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        filename = f"{timestamp}_{event_name}.jpg"

        path = os.path.join(self.folder, filename)

        cv2.imwrite(path, frame)

        return path