from aws_cdk import Stack
from constructs import Construct
from aws_cdk.aws_sqs import Queue, IQueue
from aws_cdk import Duration
from aws_cdk.aws_lambda import IFunction
from aws_cdk.aws_lambda_event_sources import SqsEventSource

class SQSQueueProps:
    def __init__(self, queue_name: str, visibility_timeout: Duration, consumer: IFunction) -> None:
        self.queue_name = queue_name
        self.visibility_timeout = visibility_timeout
        self.consumer: IFunction = consumer


class SQSQueueFactory(Construct):
    def __init__(self, scope: Construct, id: str, props: SQSQueueProps, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.id = id
        self.props: SQSQueueProps = props
        self.queue: IQueue = None
    
    def create_queue(self) -> 'SQSQueueFactory':
        self.queue = Queue(self, 
            self.id, 
            queue_name=self.props.queue_name, 
            visibility_timeout=self.props.visibility_timeout)
        return self

    def add_consumer(self, *, batch_size: int = 1) -> 'SQSQueueFactory':
        self.props.consumer.add_event_source(
            SqsEventSource(
                self.queue,
                batch_size=batch_size
            )
        )
        return self
