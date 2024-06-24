# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 13:19:49 2024

@author: juddCS
"""

import socket
import threading
import time
#import cv2

# IP and port of Tello
tello1_address = ('192.168.0.102', 8889)
tello2_address = ('192.168.0.105', 8889)
#tello3_address = ('192.168.0.105', 8889)
#tello4_address = ('192.168.0.102', 8889)
#tello5_address = ('192.168.0.100', 8889)

# IP and port of local computer
local1_address = ('192.168.0.106', 64882)
local2_address = ('192.168.0.106', 64881)
#local3_address = ('192.168.0.106', 64880)
#local4_address = ('192.168.0.106', 62982)
#local5_address = ('192.168.0.108', 62983)

# Create a UDP connection that we'll send the command to
sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock5 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the local address and port
sock1.bind(local1_address)
sock2.bind(local2_address)
#sock3.bind(local3_address)
#sock4.bind(local4_address)
#sock5.bind(local5_address)

# Send the message to Tello and allow for a delay in seconds
def send(message, delay = 3):
  # Try to send the message otherwise print the exception
  try:
    sock1.sendto(message.encode(), tello1_address)
    sock2.sendto(message.encode(), tello2_address)
    #.sendto(message.encode(), tello3_address)
    #sock4.sendto(message.encode(), tello4_address)
    #sock5.sendto(message.encode(), tello5_address)
    print("Sending message: " + message)
  except Exception as e:
    print("Error sending: " + str(e))

  # Delay for a user-defined period of time
  time.sleep(delay)
# Receive the message from Tello
def receive():
  # Continuously loop and listen for incoming messages
  while True:
    # Try to receive the message otherwise print the exception
    try:
      response1, ip_address = sock1.recvfrom(128)
      response2, ip_address = sock2.recvfrom(128)
     # response3, ip_address = sock3.recvfrom(128)
      #response4, ip_address = sock4.recvfrom(128)
      #response5, ip_address = sock5.recvfrom(128)
      decode1 = response1.decode(encoding='utf-8')
      decode2 = response2.decode(encoding='utf-8')
      #decode3 = response3.decode(encoding='utf-8')
      #decode4 = response4.decode(encoding='utf-8')
      #decode5 = response5.decode(encoding='utf-8')
      print("Received message: from Tello EDU #1: " + decode1)
      print("Received message: from Tello EDU #2: " + decode2)
      #print("Received message: from Tello EDU #3: " + decode3)
      #print("Received message: from Tello EDU #4: " + decode4)
      #print("Received message: from Tello EDU #5: " + decode5)
    except Exception as e:
      # If there's an error close the socket and break out of the loop
      print("here")
      sock1.close()
      sock2.close()
      #sock3.close()
      #sock4.close()
      #sock5.close()
      print("Error receiving: " + str(e))
      break

# Create and start a listening thread that runs in the background
# This utilizes our receive functions and will continuously monitor for incoming messages
receiveThread = threading.Thread(target=receive)
receiveThread.daemon = True
receiveThread.start()
sock1.sendto("command".encode(), tello1_address)
sock2.sendto("command".encode(), tello2_address)
sock1.sendto("takeoff".encode(), tello1_address)
sock2.sendto("takeoff".encode(), tello2_address)
delay= 3
time.sleep(delay)
listofstuff=['R','L','X','Y','U','D','P']
def opene(j):
    j = j.lower()
    for i in j:
        if i == "r":
            sock1.sendto("right 50".encode(), tello1_address)
            sock2.sendto("right 50".encode(), tello2_address)
            time.sleep(delay)
        elif i == "l":
            sock1.sendto("left 50".encode(), tello1_address)
            sock2.sendto("left 50".encode(), tello2_address)
            time.sleep(delay)
        elif i == "f":
            sock1.sendto("forward 50".encode(), tello1_address)
            sock2.sendto("forward 50".encode(), tello2_address)
            time.sleep(delay)
        elif i == "b":
            sock1.sendto("back 50".encode(), tello1_address)
            sock2.sendto("back 50".encode(), tello2_address)
            time.sleep(delay)
        elif i == "u":
            sock1.sendto("up 50".encode(), tello1_address)
            sock2.sendto("up 50".encode(), tello2_address)
            time.sleep(delay)
        elif i == "d":
            sock1.sendto("down 50".encode(), tello1_address)
            sock2.sendto("down 50".encode(), tello2_address)
            time.sleep(delay)
        elif i == "x":
            sock1.sendto("flip r".encode(), tello1_address)
            sock2.sendto("flip r".encode(), tello2_address)
            time.sleep(delay)
        elif i == "y":
            sock1.sendto("flip l".encode(), tello1_address)
            sock2.sendto("flip l".encode(), tello2_address)
            time.sleep(delay)
        elif i == "p":
           # sock1.sendto("land".encode(), tello1_address)
            sock2.sendto("land".encode(), tello2_address)
            time.sleep(delay)
        else:
            pass
while True:
    a = input()
    opene(a)
    time.sleep(5)
    send("battery?")
send("land")
print("Mission completed successfully!")

# Close the socket
sock1.close()
sock2.close()
#sock3.close()
#sock4.close()