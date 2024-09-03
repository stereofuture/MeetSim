import random

from agent import Agent

class Occupation:
    def __init__(self, name, proclivity_range, expansiveness_range, depth_range, pay_range):
        self.name = name
        self.proclivity_range = proclivity_range
        self.expansiveness_range = expansiveness_range
        self.depth_range = depth_range
        self.pay_range = pay_range

    def generate_agent(self, agent_id):
        meeting_proclivity = random.normalvariate(*self.proclivity_range)
        meeting_expansiveness = random.normalvariate(*self.expansiveness_range)
        meeting_depth = random.normalvariate(*self.depth_range)
        pay = random.normalvariate(*self.pay_range)
        return Agent(
            id=agent_id,
            meeting_proclivity=meeting_proclivity,
            meeting_expansiveness=meeting_expansiveness,
            meeting_depth=meeting_depth,
            pay=pay
        )
