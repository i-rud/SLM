from kombu import Connection

class MessageProcessor:
    @staticmethod
    def get_message() -> str:
        with Connection('amqp://guest:guest@localhost:5672//') as conn:
            try:
                simple_queue = conn.SimpleQueue('messages')
                message = simple_queue.get(block=True, timeout=0.1)
                message_to_send = message.payload
                message.ack()
                simple_queue.close()
                return message_to_send
            except Exception:
                return "No message"