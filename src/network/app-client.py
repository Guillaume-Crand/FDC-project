from network_interface import NetworkClient

network = NetworkClient()
try:
    while True:
        stop = network.treat_network_event()
        if stop:
            break


except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
