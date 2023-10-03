import pika, sys, os
import json
# test to mimic the receiver retreiving the data collected from the scrapers
def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='scraped_data')

    def callback(ch, method, properties, body):
        print(f" [x] Received %r" % json.loads(body))

    channel.basic_consume(queue='scraped_data', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)