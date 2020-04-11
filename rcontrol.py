#!/usr/bin/python3.6
#
#
# Script desenvolvido por Igor Costa Melo
# github: igorcmelo <github.com/igorcmelo>
#
#
# Utilização:
#
#
# 1) Instale as dependências
# - pynput 	(pip3 install pynput)
#
# 2) Rode o servidor na máquina que será controlada
# - por padrão ele roda na porta 1234
# - em breve adicionarei a opção de alterar a porta
# - execute: ./rcontrol.py
#
# 3) Conecte-se ao computador que será controlado
# - execute: ./rcontrol.py <ip da máquina>
# - exemplo: ./rcontrol.py 192.168.1.120
# 
# 4) Controle
# - teclas que você pressionar/soltar serão transmitidas e simulada no outro computador
# - movimentos, cliques e scrolls do mouse serão transmitidos e simulado no outro computador
#
# Observações:
# - O script foi testado apenas com dois computadores na mesma LAN.
# - O script NÃO FILTRA os comandos que recebe nem de quem recebe.
# - Uma pessoa mal intencionada poderia facilmente executar comandos
# arbitrários e ganhar acesso a sua máquina.
# - Não é recomendado utilizar numa rede na qual você não confia.

import socket
import sys

from threading import Thread
from pynput import mouse as m, keyboard as kb
from pynput.mouse import Button
from pynput.keyboard import Key


def main():

	# Se o usuário não passar argumentos ele inicia um servidor na porta 1234
	if len(sys.argv) == 1:
		port = 1234
		try:
			Server.run(port)

		except KeyboardInterrupt:
			pass

		except Exception as e:
			print("Ocorreu um erro:", e)

		print("\nServidor finalizado.")


	# Se o usuário passar um argumento, o programa irá interpretá-lo como o endereço do servidor
	elif len(sys.argv) == 2:
		port = 1234
		server = sys.argv[1]
		Client.listen()
		Client.connect(server, port)


	# Se não, mostrará a mensagem de erro
	else:
		# print()
		print("Argumentos inválidos.")
		print()
		print("Para iniciar o servidor no computador que será controlado:")
		print("	%s" % (sys.argv[0]))
		print()
		print("Para se conectar ao servidor e controlar o computador:")
		print("	%s <ENDEREÇO DO SERVIDOR>" % (sys.argv[0]))
		print()
		print()
		print("Exemplo:")
		print("  servidor:~$ ./rcontrol.py")
		print("  cliente:~$ ./rcontrol.py 192.192.168.1.120")


class Client():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	escape = False 

	# Keyboard
	def press(key):
		if Client.escape and key != Key.ctrl_r:
			return
		msg = "Server.keyboard.press(%s)" % (key)
		Client.send(msg)

	def release(key):
		if key == Key.ctrl_r:
			Client.escape = not Client.escape
			return
		msg = "Server.keyboard.release(%s)" % (key)
		Client.send(msg)

	# Mouse
	def move(x, y):
		if Client.escape:
			return
		msg = "Server.mouse.position = (%s, %s)" % (x, y)
		Client.send(msg)

	def click(x, y, button, pressed):
		if Client.escape:
			return
		action = "press" if pressed else "release"
		msg = "Server.mouse.%s(%s)" % (action, button)
		Client.send(msg)

	def scroll(x, y, dx, dy):
		if Client.escape:
			return
		msg = "Server.mouse.scroll(0, %s)" % (dy)
		Client.send(msg)

	# Handlers
	def handle_kb():
		with kb.Listener(
			on_press = Client.press, 
			on_release = Client.release) as l:
			l.join()

	def handle_mouse():
		with m.Listener(
			on_move = Client.move, 
			on_click = Client.click, 
			on_scroll = Client.scroll) as l:
			l.join()

	def listen():
		t1 = Thread(target = Client.handle_kb)
		t1.daemon = True 
		t1.start()
		t2 = Thread(target = Client.handle_mouse)
		t2.daemon = True 
		t2.start()

	def connect(server, port):
		Client.sock.connect((server, port))
		print("Conectado.")
		Client.sock.recv(1024)

	def send(msg):
		print("%s" % (msg))
		Client.sock.send(msg.encode('utf-8'))

class Server():
	mouse = m.Controller()
	keyboard = kb.Controller()

	def run(port):
		s_addr = "0.0.0.0"
		max_conns = 2
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.bind((s_addr, port))
		sock.listen(max_conns)

		print("Servidor iniciado.")
	
		while True:
			conn, addr = sock.accept()
			print("%s:%s se conectou." % (addr[0], addr[1]))

			while True:
				data = conn.recv(1024)
				if not data:
					conn.close()
					print("%s:%s se desconectou." % (addr[0], addr[1]))
					break

				print("%s" % (data.decode('utf-8')))

				try:
				 	Server.execute(data.decode())

				except Exception as e:
				 	print(e)

	def execute(msg):
		exec(msg)


if __name__ == '__main__':
	main()