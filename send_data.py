import socket

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.bind((address,port))