class NotificationObserver:
    def update(self, event, member, resource):
        raise NotImplementedError


class NotificationService(NotificationObserver):
    def __init__(self):
        self.notifications = []

    def update(self, event, member, resource):
        message = (
            f"{member.name}: {event} "
            f"'{resource.title}'"
        )

        self.notifications.append(message)

    def notify(self, event, member, resource):
        self.update(event, member, resource)

    def get_notifications(self):
        return self.notifications.copy()

    def clear(self):
        self.notifications.clear()