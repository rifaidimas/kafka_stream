from confluent_kafka import Producer
import requests
import json
import time 

url = 'https://dummyjson.com/carts'
response = requests.get(url)

carts = response.json()
 
p = Producer({'bootstrap.servers':'localhost:9092'})
print('Kafka Producer Started...')

def receipt(err,msg):
    if err is not None:
        print('Error: {}'.format(err))
    else:
        message = 'Produced message on topic {} with value of {}\n'.format(msg.topic(), msg.value().decode('utf-8'))
        print(message)

topic_name = 'carts'

def main():
    for cart in carts['carts']:
        p.produce(topic_name, json.dumps(cart).encode('utf-8'), callback=receipt)
        p.poll(1)
        p.flush()
        time.sleep(2)

if __name__ == '__main__':
    main()