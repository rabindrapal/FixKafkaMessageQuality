import logging

logger = logging.getLogger(__name__)

def send_record(producer, topic_name,message):
    message_key = int(message.get("myKey"))
    message_value = message
    try:
        producer.send(topic=topic_name, key= message_key, value=message_value)
    except Exception as e:
        logger.error(f"Exception while producing record value - {message_value}: {e}")
    else:
        logger.debug(f"Successfully produced message -{message_value}")
