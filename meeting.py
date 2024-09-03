import uuid

class Meeting:

    MIN_MEETING_LENGTH = 30
    MAX_MEETING_LENGTH = 120

    def __init__(self, scheduler, duration, participants):
        self.scheduler = scheduler
        self.duration = duration
        self.participants = participants
        self.scheduled_time = None
        self.id = uuid.uuid4()

    def schedule(self, start_time):
        self.scheduled_time = start_time

    def __repr__(self):
        return f"Meeting({self.duration} mins with {[p.id for p in self.participants]} at {self.scheduled_time})"
