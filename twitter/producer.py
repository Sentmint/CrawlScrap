import pika
import json
import os
from log_format import setup_logger

def publish_stock(stocks_found, queue_exchange, queue_key, logger):
    # Sends the found stocks to the queue  
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=os.environ.get('TWITTER_RABBITMQ_HOST')))
    channel = connection.channel()

    channel.queue_declare(queue=queue_key)

    channel.basic_publish(exchange=queue_exchange, routing_key=queue_key, body=json.dumps(stocks_found))
    logger.info(" [x] Sent Twitter Stock Data to Queue")
    connection.close()
    return