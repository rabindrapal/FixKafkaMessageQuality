## FixKafkaMessageQuality
Python application to fix UTC datetime data quality issue identified in `myTimestamp` attribute of 
messages in a Kafka topic.

### Solution
  In order to fix non UTC values of `myTimestamp` in message to expected UTC format, this application reads all 
  the input messages from the topic `input_topic`, identifies & converts the datetime format to UTC where required
  and writes all messages to `output_topic`.

### Assumptions about input data and output
* Input message loaded in the `input_topic` will be JSON format and as per specified schema.
    schema: {"myKey":integer, "myTimestamp": "string to represent date timestamp with timezone 
              offset e.g: 2022-09-04T22:31:18+01:00"}
* All messages in `input_topic` should be written in `output_topic` irrespective of data quality fix has been 
  applied to that message or not.
* Format of output message is JSON. 
*  Only `myTimestamp` value is modified for each input message where required, all other attributes of input message
   are exactly copied to corresponding output message.
  
### Expected execution environment
* Docker desktop application is pre-installed and running on host machine to test this application.
* Host machine supports unix based command line shell and has git client installed.

###
Steps to configure environment and execution of the **FixKafkaMessageQuality** application:

1. Setup application code on local 
   
   a) One command line and clone git repository for this application
      ```bash
      git clone https://github.com/rabindrapal/FixKafkaMessageQuality.git
       ```
  b) Set current working directory to base path of this application "FixKafkaMessageQuality".
    ```bash
    cd  <your-local-path>/FixKafkaMessageQuality
    ```

2. Start kafka cluster :
  Execute the below command from base directory of this application ./FixKafkaMessageQuality
    ```bash
    docker-compose up -d
   ```
3. Create required kafka topics: 
   
   a) Execute the below command to create input topic.
   ```bash
   docker exec broker \
   kafka-topics --bootstrap-server broker:9092 \
             --create \
             --topic input_topic \
             -- partitions 1
   ```
   b) Execute the below command to create output topic:
    ```bash
   docker exec broker \
   kafka-topics --bootstrap-server broker:9092 \
             --create \
             --topic output_topic \
             -- partitions 1
   ```
   
4. Start Application: Main pipeline implements the following tasks:
   * Load required input messages from `../data/input_message.json` in `input_topic` topic. 
   * Validate `myTimeStamp` field in each message and fix where required.
   * Load all messages after fix in `output_topic` topic. 
    
Execute below command to build and execute main pipeline:
   a) Containerize application code, build docker image
      ```bash
      docker build -t fix_kafka_message_quality:v0.0.1 .
        ```
   b) Execute main python application as docker in same network as of kafka server's docker and let it execute.
      ```bash
      docker run -it --network=fixkafkamessagequality_default --name FixMessageQualityApp fix_kafka_message_quality:v0.0.1
      ```

5. Verify output and input messages using different command line terminal.

   a) Read message from input topic `input_topic`
   
    ```bash
    docker exec --interactive --tty broker kafka-console-consumer --bootstrap-server broker:9092  --topic input_topic --from-beginning
      ```
   b) Read message from output topic `output_topic`
   
      ```bash
      docker exec --interactive --tty broker kafka-console-consumer --bootstrap-server broker:9092  --topic output_topic --from-beginning
      ```
   
6. Stop Application : Execute the below command to shut down services
    a) Stop main application
    
    ```bash
    docker stop FixMessageQualityApp
    ```

 b) Stop kafka services:

     ```bash
    docker compose down
    ```


### Checklist of tasks covered during implementation of this assignment:

1. Setup local Kafka cluster. Done
2. Create two kafka topics, namely `input_topic` and `output_topic`. Done
3. Populate five input message in JSON format to `input_topic` . Done
4. Build Python application to the following purpose: Done
   *  Read all messages from "input_topic".
   *  Convert current value of "myTimestamp" attribute in message to UTC format,  when available and not in UTC format.
   *   Write all messages read from `input_topic` after applying the fix where applicable to `output_topic`.
5. Containerize the application for Docker as execution engine. Done
6. Version control application code in Git hub repository. Done
     gitHub: https://github.com/rabindrapal/FixKafkaMessageQuality




