class ThreatEngine:
    """
    Determines the threat level based on surveillance events.
    """

    def __init__(self):
        pass

    def evaluate(self, event_type, class_name=None, count=0):

        # Intrusion
        if event_type == "Intrusion":
            return "HIGH"

        # Loitering
        if event_type == "Loitering":
            return "HIGH"

        # Crowd Detection
        if event_type == "Crowd":
            return "HIGH"

        # Person Detected
        if event_type == "Detection":

            if class_name == "person":
                return "MEDIUM"

            if class_name in [
                "car",
                "bus",
                "truck",
                "motorcycle",
                "bicycle"
            ]:
                return "MEDIUM"

        # Nothing detected
        return "LOW"