import pika

# Step 1: Connect to RabbitMQ server on localhost
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Step 2: Declare queue - idempotent command, can do this many times and only 1 queue will be created
channel.queue_declare(queue='hello')

# step 3: Publish (empty string = basic/default exchange)
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")

connection.close()

