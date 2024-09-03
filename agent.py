from datetime import datetime, timedelta
from meeting import Meeting
from pprint import pprint

class Agent:

    HOURS_IN_WORKDAY = 8

    def __init__(self, id, meeting_proclivity, meeting_expansiveness, meeting_depth, pay, calendar=None):
        if calendar is None:
            calendar = self.initialize_calendar()
        self.id = id
        self.meeting_proclivity = meeting_proclivity
        self.meeting_expansiveness = meeting_expansiveness
        self.meeting_depth = meeting_depth
        self.pay = pay
        self.calendar = calendar

    def __repr__(self):
        return f"Agent: {self.id}"

    # TODO: Consider using a dict with {slot, meeting}
    def initialize_calendar(self):
        # Create a calendar with 5 days of 8-hour workdays
        calendar = {}
        work_start = datetime(2024, 8, 19, 9, 0)  # Example start date
        for day in range(1):  # Monday to Friday TODO: Change this back to a week
            day_slots = []
            current_time = work_start + timedelta(days=day)
            for _ in range(int(self.HOURS_IN_WORKDAY*60/Meeting.MIN_MEETING_LENGTH)):  # 8 working hours divided into 30-minute blocks
                day_slots.append([current_time, None])  # None means free slot
                current_time += timedelta(minutes=30)
            calendar[work_start + timedelta(days=day)] = day_slots
        return calendar

    def clear_calendar(self):
        for day in self.calendar:
            for slot in self.calendar[day]:
                scheduled_event = slot[1]
                if scheduled_event is not None:
                    # print(f"Clearing {scheduled_event}")
                    slot[1]=None

    def count_meeting_time(self):
        total_meeting_time = 0
        for day in self.calendar:
            previous_meeting_id = None
            for slot in self.calendar[day]:
                scheduled_event = slot[1]
                if scheduled_event is not None and previous_meeting_id is not scheduled_event.id:
                    total_meeting_time+=scheduled_event.duration
                    previous_meeting_id = scheduled_event.id
        return total_meeting_time