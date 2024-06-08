# Kafka and Debezium utility functions
from kafka import KafkaProducer, KafkaConsumer
import json

def create_kafka_producer(config):
    """
    Create a Kafka producer
    :param config: Dictionary containing Kafka configuration
    :return: KafkaProducer object
    """
    return KafkaProducer(
        bootstrap_servers=config['bootstrap_servers'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def create_kafka_consumer(config):
    """
    Create a Kafka consumer
    :param config: Dictionary containing Kafka configuration
    :return: KafkaConsumer object
    """
    return KafkaConsumer(
        config['topic'],
        bootstrap_servers=config['bootstrap_servers'],
        auto_offset_reset=config['auto_offset_reset'],
        enable_auto_commit=config['enable_auto_commit'],
        group_id=config['group_id'],
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

def send_message(producer, topic, message):
    """
    Send a message to a Kafka topic
    :param producer: KafkaProducer object
    :param topic: Kafka topic
    :param message: Message to send
    """
    producer.send(topic, value=message)
    producer.flush()

def consume_messages(consumer):
    """
    Consume messages from a Kafka topic
    :param consumer: KafkaConsumer object
    :return: List of consumed messages
    """
    return [message.value for message in consumer]
