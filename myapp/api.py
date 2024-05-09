from flask import Flask, jsonify, request
import json
import pika
app = Flask(__name__)

@app.get('/messages')
def get_messages():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    method_frame, header_frame, body = channel.basic_get('nhung')
    if method_frame:
        channel.basic_ack(method_frame.delivery_tag)
        print(body.decode())
        json_data = json.loads(body.decode())
        address = json_data.get("address")
        if address:
            address_type_map = {
                'quan': 1,
                'ao': 2,
                'tat': 3
            }
            message = address_type_map.get(address, 4)  # Default value is 4 if address is not found
            return {'message': message}
        else:
            return {'message': ''}
    else:
        return {'message': ''}

if __name__ == "__main__":
    app.run(debug=True)