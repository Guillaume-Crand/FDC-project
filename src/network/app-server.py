from network_interface import NetworkServer

network = NetworkServer()
try:
    while True:
        network.treat_network_event()
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
