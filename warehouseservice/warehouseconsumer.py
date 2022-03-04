from kafka import KafkaConsumer, TopicPartition

def warehouseCons():
    consumer = KafkaConsumer(group_id='my-group', bootstrap_servers="127.0.0.1:9092")
    tp = TopicPartition('warehouse', 0)
    # register to the topic
    consumer.assign([tp])
    return consumer