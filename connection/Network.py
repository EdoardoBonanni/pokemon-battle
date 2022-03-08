import socket
import pickle


class Network:
    """
    Network class is the client interface that communicates with the server.
    """
    def __init__(self):
        # Create the socket and set the TCP connection between client-server.
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        self.server = str(local_ip)
        self.port = 5556
        self.addr = (self.server, self.port)
        self.player = self.connect_player()

    def get_player(self):
        """
        Get the player if exists else None.
        :return: [Player, None]
        """
        if self.player:
            return self.player
        else:
            return None

    def connect_player(self):
        """
        Try to connect client to the server and waiting to check for player id.
        :return: Return player id.
        """
        try:
            self.socket_client.connect(self.addr)
            return self.socket_client.recv(2048).decode()
        except:
            pass

    def send_receive(self, data):
        """
        Send/Receive data to/from the server.
        :param data: Data to send.
        :return: Data received.
        """
        try:
            self.socket_client.send(str.encode(data))
            return pickle.loads(self.socket_client.recv(2048*2))
        except socket.error as e:
            print(e)

