import numpy as np
import base64

from stega.injector import Injector
from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerMixin
from decoder import Decoder
from colorama import Fore, Style
from datetime import datetime

SPLITTER = "__+__"
rabbit_url = 'amqp://guest:guest@localhost:5672//'
decoder = Decoder()

class Worker(ConsumerMixin):
    def __init__(self, connection, queues):
        self.connection = connection
        self.queues = queues

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.queues,
                         callbacks=[self.on_message])]

    def on_message(self, body, message):
        body = body["frame"].encode('ascii')
        body = base64.b64decode(body)
        
        np_array = np.frombuffer(body, dtype=np.uint8)
        np_array = np_array.reshape((720, 1280, 3))

        decoded_message = Injector.pull_out_message_from_image(np_array)
        if decoded_message != "No message":
            splitted = decoded_message.split(SPLITTER)
            username = splitted[0]
            encoded_message = splitted[1]
            time = datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")
            print(f"{Fore.MAGENTA}[{time}] {Fore.CYAN}{username}{Style.RESET_ALL}: {decoder.decrypt(username, encoded_message)}")

        message.ack()

def run():
    exchange = Exchange("video-exchange", type="direct")
    queues = [Queue("frames", exchange, routing_key="video")]
    with Connection(rabbit_url, heartbeat=4) as conn:
            worker = Worker(conn, queues)
            worker.run()

if __name__ == "__main__":
    run()