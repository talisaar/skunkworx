import pika

# Step 1: Connect to RabbitMQ server on localhost
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Step 2: Declare queue - idempotent command, can do this many times and only 1 queue will be created
channel.queue_declare(queue='send_activation_link')

# step 3: Publish (empty string = basic/default exchange)
email = 'email@email.com'

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=email)
print(f" [x] Sent email to {email}")

connection.close()

