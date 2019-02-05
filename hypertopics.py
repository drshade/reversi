from game import Reversi
import time, os, json, random
import kafka

# Grab environment variables
#
brokers = os.environ.get("brokers", "127.0.0.1:9092")
to_topic = os.environ.get("to_topic", "games2")

print ("brokers=%s"%(brokers))
print ("to_topic=%s"%(to_topic))

if __name__ == "__main__":
	# Create topics
	client_id = "hyperadmin"
	admin = kafka.admin.KafkaAdminClient(bootstrap_servers=brokers, client_id=client_id)

	print("Deleting topic...")
	admin.delete_topics([to_topic])

	#print("Creating topic...")
	#topic = kafka.admin.NewTopic(to_topic, 3, 1)
	#admin.create_topics(new_topics=[topic], validate_only=True)

	admin.close()
