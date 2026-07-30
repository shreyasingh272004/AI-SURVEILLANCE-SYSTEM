import csv
import os
from datetime import datetime


class EventLogger:

    def __init__(self):

        self.log_file = "logs/events.csv"

        os.makedirs("logs", exist_ok=True)

        if not os.path.exists(self.log_file):

            with open(self.log_file, "w", newline="") as file:

                writer = csv.writer(file)

                writer.writerow([
                    "Timestamp",
                    "Event",
                    "Track ID",
                    "Class",
                    "Threat"
                ])

    def log_event(
        self,
        event_type,
        track_id,
        class_name,
        threat_level
    ):

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.log_file, "a", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                timestamp,
                event_type,
                track_id,
                class_name,
                threat_level
            ])