from datetime import datetime


class Hold:
    def __init__(self, member, resource):
        self.member = member
        self.resource = resource
        self.placed_at = datetime.now()
        self.status = "waiting"

    @property
    def is_waiting(self):
        return self.status == "waiting"

    @property
    def is_ready(self):
        return self.status == "ready"

    @property
    def is_fulfilled(self):
        return self.status == "fulfilled"

    @property
    def is_cancelled(self):
        return self.status == "cancelled"

    def mark_ready(self):
        if not self.is_waiting:
            raise ValueError("Only waiting holds can be marked ready.")

        self.status = "ready"

    def mark_fulfilled(self):
        if not self.is_ready:
            raise ValueError("Only ready holds can be fulfilled.")

        self.status = "fulfilled"

    def cancel(self):
        if self.is_fulfilled:
            raise ValueError("A fulfilled hold cannot be cancelled.")

        self.status = "cancelled"

