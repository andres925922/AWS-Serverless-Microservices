from typing import List, Dict, Union
from constructs import Construct
from aws_cdk.aws_events import EventBus, Rule, EventPattern
from aws_cdk.aws_lambda import IFunction
from aws_cdk.aws_events_targets import LambdaFunction, SqsQueue
from aws_cdk.aws_sqs import IQueue

class EventBusFactory(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.id = id
        self.rules: Dict[str, Rule] = {}

    def create_event_bus(self, name) -> 'EventBusFactory':
        """
        Create an event bus for the e-commerce microservice.
        """
        self.event_bus = EventBus(
            self, self.id,
            event_bus_name=name
        )
        return self
    
    def attach_rule(self, rule_id: str, desc: str, souces: List[str], detail_types: List[str]) -> 'EventBusFactory':
        """
        Create an event rule for the e-commerce microservice.
        """
        rule = Rule(
            self,rule_id,
            event_bus=self.event_bus,
            enabled=True,
            description=desc,
            event_pattern=EventPattern(
                source=souces,
                detail_type=detail_types
            ),
            rule_name=rule_id,
        )
        self.rules[rule_id] = rule
        return self
    
    def add_target(self, rule_id: str, target: IFunction) -> 'EventBusFactory':
        """
        Add a target to the event rule.
        """
        rule = self.rules.get(rule_id, None)
        if rule:
            rule.add_target(LambdaFunction(target))
            return self
        else:
            raise ValueError(f"Rule {rule_id} not found.")
        
    def add_sqs_target(self, rule_id: str, queue: IQueue) -> 'EventBusFactory':
        """
        Add an SQS target to the event rule.
        """
        rule = self.rules.get(rule_id, None)
        if rule:
            rule.add_target(SqsQueue(queue))
            return self
        else:
            raise ValueError(f"Rule {rule_id} not found.")
        
    def grant_publish_permissions(self, source: IFunction) -> 'EventBusFactory':
        """
        Grant publish permissions to the event bus.
        """
        self.event_bus.grant_put_events_to(source)
        return self