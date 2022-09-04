
from kafka import KafkaProducer, KafkaConsumer
from json import loads,dumps,load
import logging
from utils import KafkaUtils,DateTimeUtils
from constant import INPUT_TOPIC_NAME,OUTPUT_TOPIC_NAME,INPUT_FILE_NAME,KAFKA_BROKER
logger = logging.getLogger(__name__)

# KAFKA_BROKER = "broker:29092"
# INPUT_TOPIC_NAME = "input_topic"
# OUTPUT_TOPIC_NAME = "output_topic"
# EXPECTED_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
# INPUT_FILE_NAME="/app/data/input_message.json"


def load_json_message_from_file(input_file_path):
    logger.debug(f"Input file path for message - {input_file_path}")
    input_message_file = open(input_file_path)
    records = load(input_message_file)
    return records["input_messages"]

def fixMessageTimestamp (in_message):
    logger.debug(f"Input message to be fixed- {in_message}")
    fixedMessage =  in_message
    in_timestamp = in_message.get("myTimestamp")
    if DateTimeUtils.isExpectedDateFormat(in_timestamp):
        fixedMessage["myTimestamp"] = str(DateTimeUtils.convertToUTC(in_timestamp))
    logger.debug(f"Final message with applicable UTC myTimestamp value- {fixedMessage}")
    return fixedMessage

if __name__ == "__main__":
    logger.info(f"Pipeline configuration values: {KAFKA_BROKER} : {INPUT_TOPIC_NAME} : "
                f"{OUTPUT_TOPIC_NAME} : {INPUT_FILE_NAME}")

    logger.info(f"Configuring Kafka producer for JSON messages.")
    producer = KafkaProducer(bootstrap_servers=[KAFKA_BROKER],
                             key_serializer = lambda x:  dumps(x).encode('utf-8'),
                             value_serializer=lambda x: dumps(x).encode('utf-8'))

    logger.info(f"Configuring Kafka consumer for JSON message format application.")
    consumer = KafkaConsumer(INPUT_TOPIC_NAME,
                             bootstrap_servers=[KAFKA_BROKER],
                             auto_offset_reset="earliest",
                             enable_auto_commit=True,
                             group_id='consumer.group.id.data_fix_consumer.1',
                             value_deserializer=lambda x: loads(x.decode('utf-8'))
                             )

    logger.info(f"Load initial messages to input_topic.")
    messages_json = load_json_message_from_file(INPUT_FILE_NAME)
    for message in messages_json:
        KafkaUtils.send_record(producer, INPUT_TOPIC_NAME, message)

    logger.info(f"Starting consumer to apply fix to all messages from input_topic and write to output topic.")
    while(True):
        for message in consumer:
            in_message_value = message.value
            logger.info(f"Input message- {in_message_value}")
            fixed_message = fixMessageTimestamp(in_message_value)
            logger.info(f"fixed message - {fixed_message}")
            try :
                KafkaUtils.send_record(producer, OUTPUT_TOPIC_NAME, fixed_message)
                logger.info(f"Output message pushed in output topic - {fixed_message}")
            except Exception as e:
                logger.error(f"Failed to push message - {fixed_message} , in output topic. Exception {e}")
