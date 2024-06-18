import pika, sys, os


def main():

    # Step 1: Connect to RabbitMQ server on localhost
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Step 2: Declare queue - idempotent command, can do this many times and only 1 queue will be created
    channel.queue_declare(queue='hello')

    # Step 3: call back function will be called on_message_callback (see below)
    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    channel.basic_consume(queue='hello',
                        auto_ack=True,
                        on_message_callback=callback)

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


