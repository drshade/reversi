from game import Reversi
import time, os, json, random
import kafka
import boto3

# How to run kafka locally:
# docker run --rm -p 2181:2181 -p 3030:3030 -p 8081-8083:8081-8083 \
#      -p 9581-9585:9581-9585 -p 9092:9092 -e ADV_HOST=127.0.0.1 \
#      landoop/fast-data-dev:latest

# Grab environment variables
#
brokers = os.environ.get("brokers", "127.0.0.1:9092")
complete_topic = os.environ.get("complete_topic", "complete_games")

print ("brokers=%s"%(brokers))
print ("complete_topic=%s"%(complete_topic))

if __name__ == "__main__":
	# Random play
	client_id = "hypercomplete"
	consumer = kafka.KafkaConsumer(bootstrap_servers=brokers, client_id=client_id)
	consumer.subscribe(topics=[complete_topic])

	# Client of firehost
	client = boto3.client('firehose')

	for message in consumer:
		state = json.loads(message.value)
		print (state)

		response = client.put_record(
			DeliveryStreamName='reversi_random_games',
		    Record={
        		'Data': "%s\n"%(message.value)
    		}
		)
