class RestrictedZone:
    """
    Handles restricted zone detection.
    """

    def __init__(self):

        # Zone coordinates
        self.x1 = 150
        self.y1 = 300
        self.x2 = 500
        self.y2 = 470

    def is_inside(self, bbox):
        """
        Checks whether the center of a bounding box
        lies inside the restricted zone.

        bbox = (x1, y1, x2, y2)
        """

        x1, y1, x2, y2 = bbox

        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        if (
            self.x1 <= center_x <= self.x2
            and
            self.y1 <= center_y <= self.y2
        ):
            return True

        return False

    def get_coordinates(self):
        return (
            self.x1,
            self.y1,
            self.x2,
            self.y2
        )