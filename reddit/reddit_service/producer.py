import pika
import json
import os
import logging

def publish_stock(stocks_found, queue_exchange, queue_key, logging):
    # Sends the found stocks to the queue  
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=os.environ.get('REDDIT_RABBITMQ_HOST')))
    channel = connection.channel()

    channel.queue_declare(queue=queue_key) # TODO: Make this a passive queue once queue creation is handled

    channel.basic_publish(exchange=queue_exchange, routing_key=queue_key, properties=pika.BasicProperties(content_type='application/json'), body=json.dumps(stocks_found))
    
    logging.info(" [x] Sent Stock Data to Queue")
    connection.close()
    return