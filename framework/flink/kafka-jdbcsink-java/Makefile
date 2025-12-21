#
# Sandbox operations for IIoT tutorials
#

# Start foundation infrastructure.
start:
	docker compose up --detach --wait

# Publish a message to the Kafka broker.
test-publish:
	echo hello | kcat -b localhost -P -t testdrive

# Consume messages from the Kafka broker.
test-consume:
	kcat -b localhost -C -t testdrive -o end
