from abc import abstractmethod

from dataclasses import dataclass


@dataclass
class Queue:
    name: str
    max_priority: int = -1
    max_length: int = -1


@dataclass
class Message:
    payload: object
    priority: int = None


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
