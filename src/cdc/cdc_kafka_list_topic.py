from kafka import KafkaConsumer

consumer = KafkaConsumer(bootstrap_servers='localhost:29092')
topics = consumer.topics()
print("Topics available for connection:", topics)

