import os
import traceback
import random
import string
from random import randint
import json
import pika
import uuid

QUEUE_NAME = 'datagen'
if os.getenv('DG_APP_NAME', None):
    QUEUE_NAME += '.' + os.getenv('DG_APP_NAME')

class DGRpcClient(object):
    def __init__(self):
        rmq_host = os.getenv('RMQ_TIER', 'rmq')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=rmq_host))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, body):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key=QUEUE_NAME,
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=body)
        while self.response is None:
            self.connection.process_data_events()
        return self.response


def get_samples():
    try:
        data = {"action": "get"}
        dg_client = DGRpcClient()
        res = dg_client.call(json.dumps(data))
        return json.loads(res)
    except:
        traceback.print_exc()
        return []


def put_samples(records):
    data = {"action": "insert", "records": records}
    dg_client = DGRpcClient()
    res = dg_client.call(json.dumps(data))


if __name__ == "__main__":
    put_samples(5)
    print get_samples()
