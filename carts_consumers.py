
from confluent_kafka import Consumer
import json

c = Consumer({'bootstrap.servers':'localhost:9092','group.id':'python-consumer','auto.offset.reset':'earliest'})
print('Kafka Consumer Started...')

print('Available topics to consume: ', c.list_topics().topics)

c.subscribe(['carts'])
 
def main():
    while True:
        msg = c.poll(1.0) 
        if msg is None:
            continue
        if msg.error():
            print('Error: {}'.format(msg.error()))
            continue

        with open('carts.json','a') as file:
            data = msg.value().decode('utf-8')
            file.write(''.join(data))
            file.write(',')
    c.close()

if __name__ == '__main__':
    main()