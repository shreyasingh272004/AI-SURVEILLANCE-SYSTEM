class CrowdDetector:
    """
    Detects if the number of people
    exceeds a predefined threshold.
    """

    def __init__(self, threshold=3):
        self.threshold = threshold

    def detect(self, person_count):
        """
        Returns:
            False -> No crowd
            True  -> Crowd detected
        """
        return person_count >= self.threshold