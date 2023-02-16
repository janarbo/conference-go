from datetime import datetime
import json
import pika
from pika.exceptions import AMQPConnectionError
import django
import os
import sys
import time


sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "attendees_bc.settings")
django.setup()
from attendees.models import AccountVO


def update_AccountVO(ch, method, properties, body):
    content = json.loads(body)
    first_name = content["first_name"]
    last_name = content["last_name"]
    email = content["email"]
    is_active = content["is_active"]
    updated_string = content["updated"]
    updated = datetime.fromisoformat(updated_string)
    if is_active:

        obj, created = AccountVO.objects.update_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'is_active': is_active,
                'updated': updated
            }
        )
    else:
        AccountVO.objects.filter(email=email).delete()


while True:
    try:
        def main():
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
            channel = connection.channel()
            channel.exchange_declare(exchange='account_info', exchange_type='fanout')
            result = channel.queue_declare(queue='', exclusive=True)
            queue_name = result.method.queue
            channel.queue_bind(exchange='account_info', queue=queue_name)
            channel.basic_consume(
                queue=queue_name,
                on_message_callback=update_AccountVO,
                auto_ack=True,
            )

            channel.start_consuming()

        if __name__ == '__main__':
            try:
                main()
            except KeyboardInterrupt:
                print('Interrupted')
                try:
                    sys.exit(0)
                except SystemExit:
                    os._exit(0)
    except AMQPConnectionError:
        print("Could not connect to RabbitMQ")
        time.sleep(2.0)
