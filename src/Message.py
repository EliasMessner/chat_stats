import datetime


class Message:

    def __init__(self, date_time: datetime.datetime, sender: str, content: str):
        self.date_time = date_time
        self.sender = sender
        self.content = content

    def __str__(self):
        return str(self.date_time) + "\n" + self.sender + "\n" + self.content
