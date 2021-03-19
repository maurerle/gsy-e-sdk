import logging
import traceback

from multiprocessing import Process

from live_data_subscriber import generate_api_client_args_mapping
from live_data_subscriber.mqtt.oli_broker import MQTTConnection
from live_data_subscriber.websocket.consumer import WSConsumer


def main():
    logging.getLogger().setLevel(logging.INFO)
    # start WS
    create_process_nonblocking(WSConsumer)

    # start mqtt
    create_process_nonblocking(MQTTConnection)


def create_process_nonblocking(class_name):
    try:
        p = Process(target=class_name, args=())
        p.start()
    except Exception as e:
        logging.error(f"Subscriber failed with error {e}")
        logging.error(traceback.format_exc())


if __name__ == "__main__":
    main()
