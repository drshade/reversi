from game import Reversi
import time, os, json, random
import kafka

# Grab environment variables
#
brokers = os.environ.get("brokers", "127.0.0.1:9092")
to_topic = os.environ.get("to_topic", "games")

print ("brokers=%s"%(brokers))
print ("to_topic=%s"%(to_topic))

if __name__ == "__main__":
	# Random play
	client_id = "hyperconsumer"
	consumer = kafka.KafkaConsumer(bootstrap_servers=brokers, client_id=client_id)
	consumer.subscribe(topics=[to_topic])

	producer = kafka.KafkaProducer(bootstrap_servers=brokers)

	for message in consumer:
		# Receive a game state
		in_state = message.value

		# Load the game state into a game
		game = Reversi()
		game.state_from_string(in_state)

		# Check if the game might be completed already
		(complete, whitepoints, blackpoints, empty) = game.stats()

		print("Processing game -> white: %d black: %d"%(whitepoints, blackpoints))

		if complete:
			print("Game has ended")
			continue

		# Play one random move
		options = game.all_valid_placements()
		if len(options) == 0:
			game.skip()
		else:
			(chosenx, choseny) = options[random.randint(0, len(options) - 1)]
			game.place(chosenx, choseny)

		# Save the next move
		out_state = game.state_to_string()
		producer.send(to_topic, value=out_state.encode("ascii"))
		producer.flush()

	start = time.time()
	iterations = 100

	producer.close()
	consumer.close()


	end = time.time()
