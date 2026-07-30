import time


class LoiteringDetector:
    """
    Detects if a tracked person remains
    inside a restricted zone for longer
    than the allowed threshold.
    """

    def __init__(self, threshold=10):
        self.threshold = threshold
        self.entry_times = {}

    def update(self, track_id, inside_zone):
        """
        Returns:
            False -> No loitering
            True  -> Loitering detected
        """

        current_time = time.time()

        # Person enters the zone
        if inside_zone:

            if track_id not in self.entry_times:
                self.entry_times[track_id] = current_time

            elapsed = current_time - self.entry_times[track_id]

            if elapsed >= self.threshold:
                return True

            return False

        # Person left the zone
        else:

            if track_id in self.entry_times:
                del self.entry_times[track_id]

            return False