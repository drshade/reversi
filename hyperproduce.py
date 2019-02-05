from game import Reversi
import time, os, sys
import kafka

# Grab environment variables
#
brokers = os.environ.get("brokers", "127.0.0.1:9092")
to_topic = os.environ.get("to_topic", "games")

print ("brokers=%s"%(brokers))
print ("to_topic=%s"%(to_topic))

iterations = int(sys.argv[1])

if __name__ == "__main__":
	# Random play
	prod = kafka.KafkaProducer(bootstrap_servers=brokers)

	start = time.time()

	for iteration in range(iterations):
		game = Reversi()

		state = game.state_to_string()
		print(state)

		prod.send(to_topic, value=state.encode("ascii"))

	prod.flush()
	prod.close()

	end = time.time()
	print("Took %0.3fs to generate %d iterations"%(end - start, iterations))