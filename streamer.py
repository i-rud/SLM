from kombu import Connection, Exchange, Producer, Queue
from message_processor import MessageProcessor
from stega.injector import Injector

import cv2
import base64
import stega.utils as utils

rabbit_url = 'amqp://guest:guest@localhost:5672//'

conn = Connection(rabbit_url)
channel = conn.channel()

exchange = Exchange("video-exchange", type="direct", delivery_mode=1)

producer = Producer(exchange=exchange, channel=channel, routing_key="video")

queue = Queue(name="frames", exchange=exchange, routing_key="video", durable=True, exclusive=False, auto_delete=False) 
queue.maybe_bind(conn)
queue.declare()

queue = Queue(name="frames2", exchange=exchange, routing_key="video", durable=True, exclusive=False, auto_delete=False) 
queue.maybe_bind(conn)
queue.declare()

capture = cv2.VideoCapture(0)

while True:
    ret, frame = capture.read()
    if ret is True:
        message_to_send = MessageProcessor.get_message()

        message_length_info = '<|' + str(len(message_to_send)) + '|>'
        message = message_length_info + message_to_send
        bits_message = utils.string_to_bits(message)

        frame = Injector.extract_message_into_image(frame, bits_message)
        frame = base64.b64encode(frame.tobytes())
        frame = frame.decode('ascii')
        
        producer.publish({"frame": frame})

connection.close() 