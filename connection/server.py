import socket
from _thread import *
import pickle
from connection.message import Message

class Server:
    def __init__(self):
        self.server = "192.168.1.20"
        # self.port = 5555
        self.port = 5556

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def waiting(self):
        try:
            self.s.bind((self.server, self.port))
        except socket.error as e:
            str(e)

        self.s.listen(2)
        print("Waiting for a connection, Server Started")

        self.connected = set()
        self.messages = {}
        self.idCount = 0

        while True:
            # addr client port
            conn, addr = self.s.accept()
            print("Connected to:", addr)

            self.idCount += 1
            p = 0
            gameId = (self.idCount - 1)//2
            if self.idCount % 2 == 1:
                self.messages[gameId] = Message(gameId)
                print("Creating a new game...")
            else:
                self.messages[gameId].ready = True
                p = 1

            start_new_thread(self.threaded_client, (conn, p, gameId))


    def threaded_client(self, conn, p, gameId):
        global idCount
        conn.send(str.encode(str(p)))

        reply = ""
        while True:
            try:
                data = conn.recv(4096).decode()

                if gameId in self.messages:
                    message = self.messages[gameId]
                    message.check_data()

                    if not data:
                        break
                    else:
                        if data == "reset":
                            other_player = (p + 1) % 2
                            message.reset_data(other_player)
                        elif data != "get":
                            message.play(p, data)

                        conn.sendall(pickle.dumps(message))
                else:
                    break
            except:
                break

        print("Lost connection")
        try:
            del self.messages[gameId]
            print("Closing Game", gameId)
        except:
            pass
        self.idCount -= 1
        conn.close()

if __name__ == "__main__":
    server = Server()
    server.waiting()
    print('ok')




# data = {
#     "type": "team",
#     "pokemon_enemy_0": "charizard",
#     "pokemon_enemy_1": "abra",
#     "pokemon_enemy_2": "mankey",
#     "pokemon_enemy_3": "bulbasaur",
#     "pokemon_enemy_4": "mew",
#     "pokemon_enemy_5": "moltres"
# }
# data = {
#     "type": "pokemon_fainted",
#     "pokemon_active_" + str(p): "charizard",
#     "pokemon_active_" + str((p + 1) % 2): "bulbasaur",
#     "fainted_pokemon_" + str(p): "no",
#     "fainted_pokemon_" + str((p + 1) % 2): "yes",
#     "new_pokemon_" + str(p): "None",
#     "new_pokemon_" + str((p + 1) % 2): "mewtwo"
# }
# data = {
#     "type": "battle",
#     "pokemon_active_" + str(p): "charizard",
#     #"pokemon_active_" + str((p + 1) % 2): "blastoise",
#     "move_pokemon_" + str(p): "azione",
#     #"move_pokemon_" + str((p + 1) % 2): "volo",
#     "special_move_pokemon_" + str(p): "None",
#     #"special_move_pokemon_" + str((p + 1) % 2): "None",
#     "count_move_pokemon_" + str(p): "0",
#     #"count_move_pokemon_" + str((p + 1) % 2): "0",
#     "random_damage_pokemon_" + str(p): "0.8",
#     #"random_damage_pokemon_" + str((p + 1) % 2): "0.3"
# }