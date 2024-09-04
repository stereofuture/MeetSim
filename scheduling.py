import random
import numpy as np

from meeting import Meeting
from agent import Agent

# TODO: Separate out deciding to schedule and then the attempt to schedule

def generate_potential_meetings(agents):
    total_proclivity = sum(agent.meeting_proclivity for agent in agents)
    meetings_to_schedule = [
        (agent, max(1, round((agent.meeting_proclivity / total_proclivity) * (len(agents)*(Agent.HOURS_IN_WORKDAY/Meeting.MIN_MEETING_LENGTH_IN_HOURS)))))
        for agent in agents
    ]

    meeting_order = []
    for agent, count in meetings_to_schedule:
        meeting_order.extend([agent] * count)
    return meeting_order

def determine_meeting_length(scheduler):
    # Determine meeting length based on depth
    meeting_lengths = [30, 60, 90, 120]
    length_weights = [
        1 - scheduler.meeting_depth,
        scheduler.meeting_depth * 0.5,
        scheduler.meeting_depth * 0.25,
        scheduler.meeting_depth * 0.25,
    ]
    return random.choices(meeting_lengths, weights=length_weights, k=1)[0]

def determine_meeting_participants(scheduler, agents):
    # TODO: Refactor to have more meaningful meeting sizes (1:1, small range for collab (2-8), team, dept, company)
    potential_invites = agents.copy()
    potential_invites.remove(scheduler)

    agent_count = len(potential_invites)
    
    # Map meeting_expansiveness directly to a range of participants
    min_participants = 2
    max_participants = agent_count
    
    # Calculate the number of participants as a weighted average
    num_participants = round(min_participants + scheduler.meeting_expansiveness * (max_participants - min_participants))
    
    # Select participants
    return random.sample(potential_invites, num_participants)

def schedule_meetings(agents):
    # TODO: Turn this into max_num_meetings, take all proclivities and divide that into num meetings per agent
    # Then, assemble this into an array that can be randomized (maybe by proclivity again to reflect "eagerness")
    # Loop through this to set up the meetings, some agents may want meetings, but run out of meaningful people to schedule with
    
    #Create a list of agents based on the number of meetings they think should schedule
    meeting_order = generate_potential_meetings(agents)
    
    # Shuffle the meeting order to add some randomness to who schedules first
    random.shuffle(meeting_order)

    for scheduler in meeting_order:
        length = determine_meeting_length(scheduler)

        participants = determine_meeting_participants(scheduler, agents)

        # Find an available time slot for the meeting
        day = random.choice(list(scheduler.calendar.keys()))
        day_slots = scheduler.calendar[day]

        # Calculate the number of slots needed for the meeting
        slots_needed = length // meeting.MIN_MEETING_LENGTH_IN_MINUTES

        # Ensure that the meeting can fit within the day's available slots
        available_slots = [
            i for i in range(len(day_slots) - slots_needed + 1)
            if all(slot[1] is None for slot in day_slots[i:i + slots_needed])
        ]

        if not available_slots:
            print("No Open Meeting Slots")
            continue

        start_slot = random.choice(available_slots)

        meeting = Meeting(scheduler=scheduler, duration=length, participants=participants)

        # Schedule the meeting across the time slots
        for i in range(start_slot, start_slot + slots_needed):
            scheduler.calendar[day][i] = [scheduler.calendar[day][i][0], meeting]
            for participant in participants:
                if participant != scheduler:
                    if participant.calendar[day][i][1] is not None:
                        continue
                    else:
                        participant.calendar[day][i] = [participant.calendar[day][i][0], meeting]
    return agents
