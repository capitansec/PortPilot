from Config.QueueConsume import RabbitMQCallbacks
from Config.QueueContext import RabbitMQContext


def consume_queue(rabbitmq_context):
    """
    Start consuming messages from the specified queue
    """
    queue_name = rabbitmq_context.rabbit_connector.queue_name

    with rabbitmq_context as context:
        channel = context[1]

        channel.queue_declare(queue=queue_name)
        channel.basic_consume(queue=queue_name,
                              on_message_callback=RabbitMQCallbacks.process_message,
                              auto_ack=True)

        print("Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()


if __name__ == "__main__":
    mq_context = RabbitMQContext()
    consume_queue(mq_context)
