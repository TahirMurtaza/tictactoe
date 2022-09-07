
import pika,sys,os


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    
    channel.queue_declare(queue='scoring')
    
    
    def callback(ch,method,properties,body):
        print(" [x] Received %r" % body)
        
        
    channel.basic_consume(queue='scoring',on_message_callback=callback,auto_ack=True)

    print(" [x] waiting for message to exit press ctrl+c")
    channel.start_consuming()
    
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('interrupted')
        
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)