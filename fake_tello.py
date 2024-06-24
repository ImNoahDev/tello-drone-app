import threading
import time
from flask import Flask

app = Flask(__name__)

# Send the message to Tello and allow for a delay in seconds
def send(message, delay=3):
    try:
        print("Sending message:", message)
    except Exception as e:
        print("Error sending:", str(e))
    time.sleep(delay)

# Receive the message from Tello (mock function for testing)
def receive():
    while True:
        try:
            response1 = "Mock response from Tello EDU #1"
            response2 = "Mock response from Tello EDU #2"
            decode1 = response1
            decode2 = response2
            # print("Received message from Tello EDU #1:", decode1)
            # print("Received message from Tello EDU #2:", decode2)
        except Exception as e:
            print("Error receiving:", str(e))
            break

# Create and start a listening thread that runs in the background
receive_thread = threading.Thread(target=receive)
receive_thread.daemon = True
receive_thread.start()

@app.route('/command/<cmd>', methods=['GET'])
def command(cmd):
    if cmd == 'takeoff' or cmd == 'land' or cmd == 'emergency':
        send(cmd)
        return f"Sent command: {cmd}"
    elif cmd == 'battery':
        send("battery?")
        return "Requested battery status"
    else:
        return "Unknown command"

@app.route('/move/<direction>', methods=['GET'])
def move(direction):
    directions = {
        'up': 'up 50',
        'down': 'down 50',
        'left': 'left 50',
        'right': 'right 50',
        'forward': 'forward 50',
        'back': 'back 50'
    }
    if direction in directions:
        send(directions[direction])
        return f"Moved {direction}"
    else:
        return "Unknown direction"

@app.route('/flip/<direction>', methods=['GET'])
def flip(direction):
    flips = {
        'left': 'flip l',
        'right': 'flip r'
    }
    if direction in flips:
        send(flips[direction])
        return f"Flipped {direction}"
    else:
        return "Unknown flip direction"

@app.route('/')
def index():
    return open('index.html').read()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
