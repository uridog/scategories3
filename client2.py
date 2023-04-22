# Python program to translate
# speech to text and text to speech
import socket
import speech_recognition as sr


def voice_to_text():
    global MyText
    r = sr.Recognizer()
    try:
        # use the microphone as source for input.
        with sr.Microphone() as source2:

            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.2)

            # listens for the user's input
            audio2 = r.listen(source2)
            # Using google to recognize audio
            MyText = r.recognize_google(audio2)

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("unknown error occurred")


ans = " "
closeFunc = False
MyText = ""
counterOfText = 0
buf = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8820))
signUpOrLogIn = input("type-0 to sign up \n type-1 to log in")
if signUpOrLogIn == "0":
    firstname = input("enter your first name")
    lastname = input("enter your last name")
    name = input("enter username")
    s.send(("username:" + name).encode())
    data = s.recv(1024).decode()
    print(data)
    while "taken" in data:
        name = input("username taken, enter  new username")
        s.send(("username:" + name).encode())
        data = s.recv(1024).decode()
    password = input("enter password")
    userInfo = name + " " + firstname + " " + lastname + " " + password
    s.send(userInfo.encode())
    data = s.recv(1024).decode()
    print(data)
elif signUpOrLogIn == "1":
    name = input("enter username")
    s.send(("usernameold:" + name).encode())
    data = s.recv(1024).decode()

    while "found." in data:
        name = input("user not found, enter  new username")
        s.send(("username:" + name).encode())
        data = s.recv(1024).decode()
    password = input("enter password")
    s.send(("password:" + password).encode())
    data = s.recv(1024).decode()
    while "wrong:" in data:
        password = input("password is wrong, re-enter password")
        s.send(("password:" + password).encode())
        data = s.recv(1024).decode()
        print(data)
ready = input("press any key to start, press q to quit")
if "q" in ready:
    ready = "q:"
while "q:" not in ready:
    s.send("ready: indeed".encode())
    data = s.recv(1024).decode()
    print(data)
    while "The letter" not in data:
        data = s.recv(1024).decode()
        print(data)

    while "finished:" not in ans:

        try:
            print(ans)
            MyText = "@"
            while MyText == "@":
                voice_to_text()
            s.send(MyText.encode())
            ans = s.recv(buf).decode()

        except:
            pass
    print(ans)
    s.send("game done:".encode())
    ready = input("press any key to start, press q to quit")
    if "q" in ready:
        ready = "q:"
