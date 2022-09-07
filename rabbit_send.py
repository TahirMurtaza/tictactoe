import pika

# connection to localhost
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()  


# create the queue with name scoring
channel.queue_declare(queue='scoring')

channel.basic_publish(exchange='',routing_key='scoring',body='{"user":1,"score":1}')
print("[x] Sent 'scoring message'")
connection.close()