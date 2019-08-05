import sys
import socket
import threading
import json
from datetime import datetime

from parser import parse


def handle(request):
	"""
	Layer between server and business logic.
	"""
	data_str = json.dumps(parse(request))
	data_byte = bytes(data_str, 'cp1251')
	return data_byte

class BaseServer:
	"""
	Dummy threading TCP server.
	"""
	def run(self, ip='', port=81, maxclients=100):
		serv_sock = self.__create_serv_sock(ip, port, maxclients)
		cid = 0 # client identifier
		print(f'[Server on {port} port started]\n[Press CTRL+C for exit]')
		while True:
			client_sock = self.__handle_client_conn(serv_sock, cid)
			thread = threading.Thread(target=self.__serve_client, args=(client_sock, cid))
			thread.start()
			cid += 1

	def __formatted_datetime(self):
		date = datetime.now()
		return date.strftime('%d.%m.%Y %H:%M:%S')


	def __create_serv_sock(self, ip, port, maxclients):
		serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
		serv_sock.bind((ip, port))
		serv_sock.listen(maxclients)
		return serv_sock

	def __handle_client_conn(self, serv_sock, cid):
		client_sock, client_addr = serv_sock.accept()
		print(f'{self.__formatted_datetime()} Client #{cid} - {client_addr} connected')
		return client_sock

	def __serve_client(self, client_sock, cid):
		request = self.__read_request(client_sock, cid)
		if request is None:
			print(f'{self.__formatted_datetime()} Client #{cid} - disconnected')
		else:
			response = self.__handle_request(request)
			self.__send_response(client_sock, response, cid)

	def __read_request(self, client_sock, cid):
		try:
			while True:
				data = client_sock.recv(1024)
				if not data:
					return None
				return None if not data else data
		except ConnectionError:
			print(f'{self.__formatted_datetime()} Client #{cid} - unexpectedly disconnected')
			return None

	def __handle_request(self, request):
		return handle(request)

	def __send_response(self, client_sock, response, cid):
		client_sock.sendall(response)
		client_sock.close()
		print(f'{self.__formatted_datetime()} Client #{cid} - handled and disconnected')


if __name__ == '__main__':
	try:
		BaseServer().run()
	except KeyboardInterrupt:
		print('[Server stopped]\r')
		sys.exit()
	except OSError as error:
		print(error)
