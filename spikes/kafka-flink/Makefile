#
# Sandbox operations for IIoT tutorials
#

# Start foundation infrastructure.
start:
	docker-compose up

# Publish a message to the Kafka broker.
test-publish:
	echo hello | kafkacat -b localhost -P -t testdrive

# Consume messages from the Kafka broker.
test-consume:
	kafkacat -b localhost -C -t testdrive -o end
