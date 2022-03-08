import socket
from _thread import *
import pickle
from connection.Message import Message


class Server:
    """
    Server class for communication between clients.
    """
    def __init__(self):
        # Init the server.
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        self.server = str(local_ip)
        self.port = 5556
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def waiting(self):
        """
        Waiting clients and start a thread for every client for the communication.
        :return:
        """
        try:
            self.socket_server.bind((self.server, self.port))
        except socket.error as e:
            str(e)

        self.socket_server.listen(2)  # accept only two clients.
        print("Waiting for a connection, server started")

        self.connected = set()
        self.messages = {}
        self.id_count = 0

        while True:
            conn, address = self.socket_server.accept()  # address client port.
            print("Connected to:", address)

            self.id_count += 1
            player = 0
            game_id = (self.id_count - 1) // 2
            if self.id_count % 2 == 1:
                self.messages[game_id] = Message(game_id)
                print("Creating a new game...")
            else:
                player = 1

            start_new_thread(self.threaded_client, (conn, player, game_id))

    def threaded_client(self, conn, player, game_id):
        """
        Thread for client communication.
        :param conn: Socket object usable to send and receive data on the connection.
        :param player: Player 0/1.
        :param game_id: Game id for clients.
        :return:
        """
        conn.send(str.encode(str(player)))

        while True:
            try:
                data = conn.recv(4096).decode()  # data received from clients.

                if game_id in self.messages:
                    message = self.messages[game_id]  # check which client sent the message.
                    message.check_data()

                    if not data:
                        break
                    else:
                        if data == "reset":  # in this case, the moves and data are reset.
                            other_player = (player + 1) % 2
                            message.reset_data(other_player)
                        elif data != "get":  # in this case, the moves and data are sent.
                            message.send_data(player, data)
                        elif data == "get":
                            pass  # in this case, send only a message to the other client.

                        conn.sendall(pickle.dumps(message))  # this sends the messages.
                else:
                    break
            except:
                break

        print("Lost connection with a client")
        try:
            del self.messages[game_id]
            print("Closing game", game_id)
        except:
            pass
        self.id_count -= 1
        conn.close()


if __name__ == "__main__":
    server = Server()
    server.waiting()
    print('ok')
