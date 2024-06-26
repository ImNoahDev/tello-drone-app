import socket
import threading
import time
from flask import Flask, request

app = Flask(__name__)

# IP and port of Tello
tello1_address = ('192.168.0.102', 8889)
tello2_address = ('192.168.0.105', 8889)

# IP and port of local computer
local1_address = ('192.168.0.106', 64882)
local2_address = ('192.168.0.106', 64881)

# Create UDP sockets
sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind sockets to local address and port
sock1.bind(local1_address)
sock2.bind(local2_address)

# Function to send message to both Tello drones
def send(message, delay=3):
    try:
        sock1.sendto(message.encode(), tello1_address)
        sock2.sendto(message.encode(), tello2_address)
        print("Sending message:", message)
    except Exception as e:
        print("Error sending:", str(e))
    time.sleep(delay)

# Function to receive messages from both Tello drones
def receive():
    while True:
        try:
            response1, ip_address = sock1.recvfrom(128)
            response2, ip_address = sock2.recvfrom(128)
            decode1 = response1.decode('utf-8')
            decode2 = response2.decode('utf-8')
            print("Received message from Tello EDU #1:", decode1)
            print("Received message from Tello EDU #2:", decode2)
        except Exception as e:
            print("Error receiving:", str(e))
            break

# Thread for receiving messages
receive_thread = threading.Thread(target=receive)
receive_thread.daemon = True
receive_thread.start()

# Function to send battery command every 5 seconds
def send_battery_command():
    while True:
        send("battery?")
        time.sleep(5)

# Thread for sending battery command
battery_thread = threading.Thread(target=send_battery_command)
battery_thread.daemon = True
battery_thread.start()

# Flask routes
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
    app.run(host='0.0.0.0', port=5000)
