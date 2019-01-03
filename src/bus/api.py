import json
from abc import abstractmethod


class Queue:
    def __init__(self, name, max_priority=-1) -> None:
        self.name = name
        self.max_priority = max_priority


class Message:
    def __init__(self, payload, priority=None) -> None:
        super().__init__()
        self.payload = payload
        self.priority = priority

    def to_json(self):
        return json.dumps({
            'payload': json.dumps(self.payload),
            'priority': self.priority
        })

    @staticmethod
    def from_json(json_data):
        data = json.loads(json_data)
        return Message(data.get('payload'), data.get('payload'))


class Bus:
    @abstractmethod
    def send(self, queue: Queue, msg: Message):
        pass

    @abstractmethod
    def subscribe(self, queue: Queue, handler):
        pass


class Handler:
    @abstractmethod
    def handle(self, message: Message, bus: Bus):
        pass




