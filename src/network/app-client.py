from network_interface import NetworkClient


def create_request(action, value):
    if action == "search":
        return dict(
            type="text/json",
            encoding="utf-8",
            content=dict(action=action, value=value),
        )
    else:
        return dict(
            type="binary/custom-client-binary-type",
            encoding="binary",
            content=bytes(action + value, encoding="utf-8"),
        )


network = NetworkClient()
action, value = "search", "morpheus"
request = create_request(action, value)
network.send_message(request)
try:
    while True:
        stop = network.process_received_messages()
        if stop:
            break


except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
