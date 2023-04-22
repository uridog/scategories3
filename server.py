import random
import socket as so
import string
import threading
import threading as th
from queue import Queue
import time

from db import user_exists, add_user, check_password, build_db, add_score_to_user

username = ""
player_lists = []
current_start_letter = 'A'
start_game = False
lock = threading.Lock()
game_end = False
build_db()
game_data_updated = False
clients = []
clientsReady = []
conn_q = Queue()
buf = 1024
file = open("countries.txt")
countriesList = file.read().split("\n")
file2 = open("cities.txt")
citiesList = file2.read().split("\n")
file3 = open("boy.txt")
boyList = file3.read().split("\n")
movieList = []
file4 = open("movies.txt")
long_movie_List = file4.read().split("\n")
for z in long_movie_List:
    position = z.find("(")
    z = z[:(position - 1)]
    movieList.append(z)
file5 = open("animals.txt", encoding="utf8")
animalsList = file5.read().split("\n")
file6 = open("fruitsAndVeggies.txt")
fruitsAndVeggiesList = file6.read().split("\n")
file7 = open("householdItems.txt")
householdItemsList = file7.read().split("\n")


def infinite_random_letters():
    while True:
        letter = random.choice(string.ascii_uppercase)
        if letter != 'X' or letter != 'Y' or letter != 'Z' or letter != 'Q' or letter != 'W' or letter != 'F':
            yield letter


def infinite_letters():
    random_letters = infinite_random_letters()

    return random_letters


def log_in(data, client_socket):
    global clientsReady
    global username
    global clients
    if "username:" in data:
        while user_exists(data.split(":")[1]) is True:
            client_socket.send("Username is already taken".encode())
            data = client_socket.recv(1024).decode()
        username = data.split(":")[1]
        client_socket.send("Accepted".encode())
        data = client_socket.recv(1024).decode()
        add_user(data.split()[0], data.split()[1], data.split()[2], data.split()[3])
        if len(clients) == 3:
            client_socket.send("User added but game is currently full".encode())
        while len(clients) == 3:
            pass
        clients.append([client_socket, data.split()[0]])
        clientsReady.append([clients[-1], False])
        print(clients)
        client_socket.send("Accepted".encode())
    if "usernameold:" in data:
        while user_exists(data.split(":")[1]) is not True:
            client_socket.send("user not found.".encode())
            data = client_socket.recv(1024).decode()
        username = data.split(":")[1]
        if len(clients) == 3:
            client_socket.send("Game is currently full".encode())
        while len(clients) == 3:
            pass
        client_socket.send("Accepted".encode())
        data = client_socket.recv(1024).decode()
        while check_password(username, data.split(":")[1]) is not True:
            client_socket.send("password is wrong: ".encode())
            data = client_socket.recv(1024).decode()
        client_socket.send("Accepted".encode())
        clients.append((client_socket, username))
        clientsReady.append([clients[-1][1], False])
    return username


def broadcast(string_to_broadcast, clientList):
    for i in clientList:
        i[0].send(string_to_broadcast.encode())


def check_if_ready(clientList):
    for i in clientList:
        if i[1] is False:
            return False
    return True


def handle_client(client_socket):
    global current_start_letter
    global clients
    global start_game
    global clientsReady
    global game_end
    global game_data_updated
    categories_arr = [0, 0, 0, 0, 0, 0, 0]
    word_arr = ["", "", "", "", "", "", ""]
    print("222", th.get_native_id())
    """Handles a single client connection."""
    data = client_socket.recv(1024).decode()
    print(data)
    client_name = log_in(data, client_socket)
    # ready message
    data = client_socket.recv(1024).decode()
    if "ready:" in data:
        for c in clientsReady:
            if c[0] == client_name:
                c[1] = True
    while "q:" not in data:
        game_end = False
        added_list = False
        msgSent = False
        msgToSend = ""
        while start_game is False:
            pass
        data = client_socket.recv(1024).decode()
        while "done:" not in data:
            try:

                myText = data.lower()
                myText = myText.title()
                myTextListAllWords = myText.split(" ")
                myTextList = [word for word in myTextListAllWords if word.startswith(current_start_letter)]
                plural_list = []
                for q in myTextList:
                    plural_list.append(q+"s")
                myTextList = myTextList + plural_list
                myTextList.append(myText)
                for i in countriesList:
                    if i in myTextList:
                        print("you said a country")
                        msgToSend = "you said a country"
                        categories_arr[0] = 1
                        word_arr[0] = i
                        msgSent = True
                        break
                for x in citiesList:
                    if x in myTextList:
                        print("you said a capital")
                        if msgSent is False:
                            msgToSend = "you said a capital"
                        else:
                            msgToSend += " and also a capital"
                        categories_arr[1] = 1
                        word_arr[1] = x
                        msgSent = True
                        break
                for j in boyList:
                    if j in myTextList:
                        print("you said a boy")
                        if msgSent is False:
                            msgToSend = "you said a boy"
                        else:
                            msgToSend += " and also a boy"
                        categories_arr[2] = 1
                        word_arr[2] = j
                        msgSent = True
                        break
                for p in movieList:
                    if p in myTextList:
                        print("you said a movie")
                        if msgSent is False:
                            msgToSend = "you said a movie"
                        else:
                            msgToSend += " and also a movie"
                        categories_arr[3] = 1
                        word_arr[3] = p
                        msgSent = True
                        break
                for t in animalsList:
                    if t in myTextList:
                        print("you said an animal")
                        if msgSent is False:
                            msgToSend = "you said a animal"
                        else:
                            msgToSend += " and also a animal"
                        categories_arr[4] = 1
                        word_arr[4] = t
                        msgSent = True
                        break
                for n in fruitsAndVeggiesList:
                    if n in myTextList:
                        print("you said a fruit/vegetable")
                        if msgSent is False:
                            msgToSend = "you said a fruit/vegetable"
                        else:
                            msgToSend += " and also a fruit/vegetable"
                        categories_arr[5] = 1
                        word_arr[5] = n
                        msgSent = True
                        break
                for b in householdItemsList:
                    if b in myTextList:
                        print("you said a household item")
                        if msgSent is False:
                            msgToSend = "you said a household item"
                        else:
                            msgToSend += " and also a household item"
                        categories_arr[6] = 1
                        word_arr[6] = b
                        msgSent = True
                        break
                if categories_arr[6] != 1:
                    for v in myTextList:
                        if v in householdItemsList:
                            print("you said a household item")
                            if msgSent is False:
                                msgToSend = "you said a household item"
                            else:
                                msgToSend += " and also a household item"
                            categories_arr[6] = 1
                            word_arr[6] = v
                            msgSent = True
                            break

                print("Did you say ", myText)

                if 0 not in categories_arr:
                    broadcast("A player finished: ending game", clients)
                    player_lists.append((word_arr, client_name))
                    added_list = True
                else:
                    if msgSent is True:
                        client_socket.send(msgToSend.encode())
                    else:
                        client_socket.send(" ".encode())
                    msgSent = False
                    msgToSend = ""
                data = client_socket.recv(1024).decode()
            except:
                pass
        if added_list is False:
            player_lists.append((word_arr, client_name))
        game_end = True
        while game_data_updated is False:
            pass
        for i in clientsReady:
            i[1] = False
        categories_arr = [0, 0, 0, 0, 0, 0, 0]
        word_arr = ["", "", "", "", "", "", ""]


def main():
    global current_start_letter
    global start_game
    global game_data_updated
    client_num = 0
    only_word_in_category_equals_15 = True
    special_word_equals_10 = True
    print("Start Server")
    server_socket = so.socket()
    server_socket.bind(('0.0.0.0', 8820))
    server_socket.listen(1)
    letters = infinite_letters()
    while client_num < 3:
        (client_socket, client_address) = server_socket.accept()
        try:
            e = th.Thread(target=handle_client, args=(client_socket,))
            e.start()
            client_num += 1
        except:
            pass

    while check_if_ready(clientsReady) is False or len(clientsReady) < 3:
        pass
    game_data_updated = False
    start_game = True
    broadcast("game staring in 3..", clients)
    time.sleep(1)
    broadcast("2", clients)
    time.sleep(1)
    broadcast("1", clients)
    time.sleep(1)
    current_start_letter = next(letters)
    broadcast("The letter is " + current_start_letter + ".", clients)
    while game_end is False:
        pass
    while len(player_lists) < 3:
        pass
    for i in player_lists:
        for t in i[0]:
            if t != "":
                word = t
                for x in player_lists:
                    if x != i:
                        for w in x[0]:
                            if w != "":
                                only_word_in_category_equals_15 = False
                            if only_word_in_category_equals_15 is False:
                                if w == word:
                                    special_word_equals_10 = False
            if only_word_in_category_equals_15 is True:
                add_score_to_user(i[1], 15)
            elif special_word_equals_10 is True:
                add_score_to_user(i[1], 10)
            else:
                add_score_to_user(i[1], 5)
            only_word_in_category_equals_15 = True
            special_word_equals_10 = True
    game_data_updated = True


main()
