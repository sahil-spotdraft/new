from collections import defaultdict
from typing import List


class Issue:
    def __init__(self, id, order_id, issue_type, description):
        self.id = id
        self.order_id = order_id
        self.issue_type = issue_type
        self.description = description

class Agent:
    def __init__(self, id, expertise):
        self.id = id
        self.expertice = expertise

class AssignManager:
    def __init__(self):
        self.agent_to_issue_ids_map = defaultdict(list)
        self.assign_strategies = []

    def assign_issue(self, issue, assign_strategy, issue_types, agents):
        

class IssueResolution:
    def __init__(self, issue_types: List[str]):
        if len(set(issue_types)) > 20:
            raise ValueError
        self.issue_types = set(issue_types)
        self.issues = {}
        self.agents = {}
        self.assign_manager = AssignManager()

    def create_issue(self, issue_id, order_id, issue_type, description):
        self.issues[issue_id] = Issue(
            issue_id, order_id, issue_type, description
        )
        
    def add_agent(self, agent_id, expertise):
        self.agents[agent_id] = Agent(agent_id, expertise)

    def assign_issue(self, issue_id, assign_strategy):
        self.assign_manager.assign_issue(
            self.issues[issue_id], assign_strategy, self.issue_types, self.agents.values()
        )