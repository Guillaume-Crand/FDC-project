from network_interface import NetworkServer

network = NetworkServer()
try:
    while True:
        network.process_received_messages()
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
