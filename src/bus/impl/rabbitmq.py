import pika

from bus.api import Bus, Handler, Message, Queue


class RmqBus(Bus):

    def __init__(self, host) -> None:
        super().__init__()
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()

    def send(self, queue: Queue, msg):
        self._ensure_queue(queue)
        self.channel.basic_publish(exchange='',
                                   routing_key=queue.name,
                                   body=self._serialize_msg(msg))

    def subscribe(self, queue: Queue, handler: Handler):
        print("Registered handler %s on queue %s (max_priority=%s)" % (handler, queue.name, queue.max_priority))

        def internal_handle(ch, method, properties, body):
            handler.handle(self._deserialize_msg(body), self)

        self._ensure_queue(queue)
        self.channel.basic_consume(internal_handle,
                                   queue=queue.name,
                                   no_ack=True)

    def _ensure_queue(self, queue: Queue):
        args = None
        if queue.max_priority > 0:
            args = {'x-max-priority': queue.max_priority}
        self.channel.queue_declare(queue=queue.name, arguments=args)

    @staticmethod
    def _serialize_msg(msg: Message) -> str:
        return msg.to_json()

    @staticmethod
    def _deserialize_msg(serialized) -> Message:
        return Message.from_json(serialized)

    def start_consuming(self):
        self.channel.start_consuming()
