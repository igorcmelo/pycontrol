#!/usr/bin/python3.6

import socket, sys
from sys import stderr
from threading import Thread 
from pynput import keyboard as k, mouse as m
from pynput.keyboard import Key
from pynput.mouse import Button


def main():
	port = 1234 # you can change this

	# server
	if len(sys.argv) == 1:
		addr = "0.0.0.0"
		server = Server(addr, port)

	# client
	elif len(sys.argv) == 2:
		addr = sys.argv[1]
		client = Client(addr, port)

	# error
	else:
		print()
		print("[ERROR] Invalid number of args.")
		print()
		usage()


def usage():
	print("Usage:")
	print("  (server): %s" % sys.argv[0])
	print("  (client): %s <server_address>" % sys.argv[0])
	print()
	print()


# The computer that will be controlled
class Server:
	def __init__(self, s_addr, port):
		self.max_cons = 1 # you can change this (I never tried with more than 1 client)

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind((s_addr, port))
		self.sock.listen(self.max_cons)

		print("[INFO] Server is up.")

		keyboard = k.Controller()
		mouse = m.Controller()

		# keep accepting clients
		while True:
			conn, c_addr = self.sock.accept()
			c_ip = c_addr[0]
			c_port = c_addr[1]
			print("[INFO] %s:%s connected." % (c_ip, c_port))


			# receive the commands
			while True:
				data = conn.recv(1024)
				if not data:
					conn.close()
					print("[INFO] %s:%s disconnected." % (c_ip, c_port))
					break

				cmd = data.decode('utf-8')
				print(cmd)

				try:
					exec(cmd) # THIS IS DANGEROUS! BE CAREFUL!

				except Exception as e:
					stderr.write("[ERROR] " + str(e))


# The computer that will control another computer
class Client:
	def __init__(self, addr, port, escapekey = Key.ctrl_r):
		self.escape = False
		self.escapekey = escapekey
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((addr, port))

		th_keyboard = Thread(target = self.listen_keyboard)
		th_keyboard.daemon = True
		th_keyboard.start()

		th_mouse = Thread(target = self.listen_mouse)
		th_mouse.start()


	# ------- KEYBOARD EVENTS ------- #
	def press(self, key):
		msg = "keyboard.press(%s)" % (key)

		if self.escape: 
			print("[IGNORING] " + msg)
			return

		self.send(msg)

	def release(self, key):
		if key == self.escapekey: 
			self.escape = not self.escape
			return 

		msg = "keyboard.release(%s)" % (key)

		if self.escape: 
			print("[IGNORING] " + msg)
			return

		self.send(msg)


	# ------- MOUSE EVENTS ------- #
	def move(self, x, y):
		msg = "mouse.position = (%s, %s)" % (x, y)
		if self.escape: 
			print("[IGNORING] " + msg)
			return

		self.send(msg)

	def click(self, x, y, button, pressed):
		msg = "mouse.click(%s)" % (button)
		if self.escape: 
			print("[IGNORING] " + msg)
			return

		self.send(msg)	

	def scroll(self, x, y, dx, dy):
		msg = "mouse.scroll(%s, %s)" % (dx, dy)
		if self.escape: 
			print("[IGNORING] " + msg)
			return

		self.send(msg)	


	# ------- EVENT LISTENERS ------- #
	def listen_mouse(self):
		with m.Listener(
				on_move = self.move, 
				on_click = self.click, 
				on_scroll = self.scroll) as l:
			l.join()

	def listen_keyboard(self):
		with k.Listener(
				on_press = self.press, 
				on_release = self.release
		) as l:
			l.join()


	# ------- SEND MESSAGES THROUGH SOCKET ------- #
	def send(self, msg):
		print(msg)
		self.sock.send(msg.encode('utf-8'))


if __name__ == '__main__':
	main()