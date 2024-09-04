from agent import Agent
from meeting import Meeting

#TODO: Consider moving to util to DRY
# Example Agent class for testing
def create_test_agent(id, depth=0, expansiveness=0, proclivity=0):
    calendar={
            'Monday': [[30 * i, None] for i in range(int(Agent.HOURS_IN_WORKDAY*60/Meeting.MIN_MEETING_LENGTH_IN_MINUTES))],  # 8-hour workday
            'Tuesday': [[30 * i, None] for i in range(int(Agent.HOURS_IN_WORKDAY*60/Meeting.MIN_MEETING_LENGTH_IN_MINUTES))],
        }
    
    return Agent(id=id, meeting_depth=depth, meeting_expansiveness=expansiveness, meeting_proclivity=proclivity, pay=10000, calendar=calendar)

def test_count_meeting_time():
    agent = create_test_agent(id=1)
    for day in agent.calendar:
        for slot in agent.calendar[day]:
            slot[1] = Meeting(scheduler=agent, duration=30, participants=[])

    max_meeting_time = Meeting.MIN_MEETING_LENGTH_IN_MINUTES*16*2

    assert agent.count_meeting_time() == max_meeting_time

def test_clear_calendar():
    agent = create_test_agent(id=1)
    for day in agent.calendar:
        for slot in agent.calendar[day]:
            slot[1] = Meeting(scheduler=agent, duration=30, participants=[])

    max_meeting_time = Meeting.MIN_MEETING_LENGTH_IN_MINUTES*16*2

    assert agent.count_meeting_time() == max_meeting_time

    agent.clear_calendar()

    assert agent.count_meeting_time() == 0
            