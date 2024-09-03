import pytest
import random
from agent import Agent

from scheduling import determine_meeting_length, determine_meeting_participants, generate_potential_meetings

# Example Agent class for testing
def create_test_agent(id, depth=0, expansiveness=0, proclivity=0):
    calendar={
            'Monday': [(30 * i, None) for i in range(16)],  # 8-hour workday
            'Tuesday': [(30 * i, None) for i in range(16)],
        }
    
    return Agent(id=id, meeting_depth=depth, meeting_expansiveness=expansiveness, meeting_proclivity=proclivity, pay=10000, calendar=calendar)

# Assume determine_meeting_length is defined above
@pytest.mark.parametrize("id, depth, expected_length", [
    (1, 0.0, 30),
    (2, 0.1, 30),
    (3, 0.2, 60),
    (4, 0.3, 60),
    (5, 0.4, 90),
    (6, 0.5, 90),
    (7, 0.6, 90),
    (8, 0.7, 120),
    (9, 0.8, 120),
    (10, 0.9, 120),
    (11, 1.0, 120)
])
def test_determine_meeting_length_parameterized(id, depth, expected_length):
    random.seed(0)  # Set the random seed for reproducibility

    scheduler = create_test_agent(id=id, depth=depth)
    length = determine_meeting_length(scheduler)
    
    assert length == expected_length, f"With seed 0 and depth {depth}, expected {expected_length}-minute meeting but got {length}."


@pytest.mark.parametrize("expansiveness, expected_participant_ids", [
    (0.0, [6, 9]),
    (0.1, [6, 9, 0]),
    (0.2, [6, 9, 0, 2]),
    (0.3, [6, 9, 0, 2]),
    (0.4, [6, 9, 0, 2, 4]),
    (0.5, [6, 9, 0, 2, 4, 3]),
    (0.6, [6, 9, 0, 2, 4, 3, 5]),
    (0.7, [6, 9, 0, 2, 4, 3, 5, 1]),
    (0.8, [6, 9, 0, 2, 4, 3, 5, 1]),
    (0.9, [6, 9, 0, 2, 4, 3, 5, 1, 8]),
    (1.0, [6, 9, 0, 2, 4, 3, 5, 1, 8, 7])
])
def test_determine_meeting_participants_parameterized(expansiveness, expected_participant_ids):
    random.seed(0)  # Set the random seed for reproducibility
    
    # Create a list of 10 agents with IDs 0 to 9
    agents = [create_test_agent(id=i) for i in range(10)]
    
    # Create a scheduler with the given expansiveness
    scheduler = create_test_agent(id=99, expansiveness=expansiveness)

    agents.append(scheduler)
    
    participants = determine_meeting_participants(scheduler, agents)

    participant_ids = [participant.id for participant in participants]
    
    # Comparing the list allows us to check that we aren't scheduling agents
    # more than once or scheduling the scheduler
    assert participant_ids == expected_participant_ids, (
        f"Expansiveness {expansiveness}, expected participant IDs "
        f"{expected_participant_ids}, got {participant_ids}."
    )


def test_generate_potential_meetings():
    agents = [create_test_agent(id=i, proclivity=(i*0.1)) for i in range(6)]

    meeting_schedulers = generate_potential_meetings(agents)
    expected_potential_meetings = 97
    print(meeting_schedulers)

    assert len(meeting_schedulers) == expected_potential_meetings