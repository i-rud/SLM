from kombu import Connection, Exchange, Producer, Queue

class RabbitMQUtils:
    def __init__(self):
        self.rabbit_url = 'amqp://guest:guest@localhost:5672//'
        self.conn = Connection(self.rabbit_url)
        self.channel = self.conn.channel()
        self.exchange = Exchange("message", type="direct", delivery_mode=1)
        self.producer = Producer(exchange=self.exchange, channel=self.channel)
        self.queue = Queue(name="messages", exchange=self.exchange, durable=True, exclusive=False, auto_delete=False) 
        self.queue.maybe_bind(self.conn)
        self.queue.declare()

    def send_message(self, message):
        self.producer.publish(message)

    def close_connection(self):
        self.conn.close()