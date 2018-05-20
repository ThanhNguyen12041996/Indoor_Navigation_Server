
import firebase_admin
import scipy.io
import numpy as np
from firebase import firebase
from firebase_admin import credentials
from firebase_admin import db


"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from RadarCoorEstimateAppdroach import Radar
from LWPApproach import WKNN
mat = scipy.io.loadmat('IndoorNav2018.mat')

CoordinatesTrainData = mat['CoordinatesTrainData']
CoordinatesTestData = mat['CoordinatesTestData']
DataTrain = mat['DataCuoiTrain']
DataTest = np.array([[-68,-79,-90,-80,-84,-89,-85,-84,-90,-91,-77,-74,-110,-90,-81,-82,-110,-110,-110,-110,-110,-110,-110,-110,-110,-110,-110,-110,-110,-110,-110,-110]])

max_X = 10.7629254700000
max_Y = 106.682092800000
min_X = 10.7623750800000
min_Y = 106.681507800000

firebase = firebase.FirebaseApplication("https://indoornavigationdatabase.firebaseio.com")

# """Get data from Firebase"""
# result = firebase.get('/Data','Latitude')
# """push data into Firebase"""
# resultput = firebase.put('/Data','RSS','-90')
# print("result la",result)


cred = credentials.Certificate("indoornavigationdatabase-firebase-adminsdk-h5z5q-4a356180a1.json")
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {"databaseURL": "https://indoornavigationdatabase.firebaseio.com"})
root = db.reference()
print(root.get())

def call_function(message):
  print( message["event"])
  print(message["path"])
  print("RSS: ",db.reference("Data").child("RSS").get())
  result = db.reference("Data").child("RSS").get()
  results = list(map(int, result.split()))
  res = np.array([results])
  t = MinMaxCoorEst(WKNN(DataTrain,CoordinatesTrainData,res,2))
  firebase.put('/Data','Latitude',t[0,0])
  firebase.put('/Data','Longtitude',t[0,1])


my_stream_question_requested = db.reference("Data").child("RSS").stream(call_function, stream_id="new stream")

# new_user = root.child("Data").push({"RSS": "lila Annen", "Latitude": 19})
# ref = root.child("Data")
# print(ref.get())

def MinMaxCoorEst(CoorsEst):
    if CoorsEst[0,0] <= min_X:
        CoorsEst[0,0] = min_X
    else:
        if CoorsEst[0,0] >= max_X:
            CoorsEst[0,0] = max_X
    if CoorsEst[0,1] <= min_Y:
        CoorsEst[0,1] = min_Y
    else:
        if CoorsEst[0,1] >= max_Y:
            CoorsEst[0,1] = max_Y

    return CoorsEst


# def accept_incoming_connections():
#     # t = MinMaxCoorEst(Radar(DataTrain, CoordinatesTrainData, DataTest, 2))
#     # print(t)
#
#     """Sets up handling for incoming clients."""
#     while True:
#         client, client_address = SERVER.accept()
#         print("%s:%s has connected." % client_address)
#         client.send(bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
#         addresses[client] = client_address
#         Thread(target=handle_client, args=(client,)).start()
#
#
# def MinMaxCoorEst(CoorsEst):
#     if CoorsEst[0,0] <= min_X:
#         CoorsEst[0,0] = min_X
#     else:
#         if CoorsEst[0,0] >= max_X:
#             CoorsEst[0,0] = max_X
#     if CoorsEst[0,1] <= min_Y:
#         CoorsEst[0,1] = min_Y
#     else:
#         if CoorsEst[0,1] >= max_Y:
#             CoorsEst[0,1] = max_Y
#
#     return CoorsEst
#
# def handle_client(client):  # Takes client socket as argument.
#     """Handles a single client connection."""
#
#     # name = client.recv(1024).decode("utf8")
#     # welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
#     # client.send(bytes(welcome, "utf8"))
#     # msg = "%s has joined the chat!" % name
#     # broadcast(bytes(msg, "utf8"))
#     clients[client] = "A"
#
#     while True:
#         msg = client.recv(1024)
#         if len(msg) != 2:
#             result = msg.decode()
#
#             print("size la: ",len(msg))
#             print("mang nhan dc",result)
#             results = list(map(int, result.split()))
#             res = np.array([results])
#             t = MinMaxCoorEst(WKNN(DataTrain,CoordinatesTrainData,res,2))
#             print(t)
#
#             stringTosend = (str(t[0,0])+","+str(t[0,1]) + "\n")
#             client.send(stringTosend.encode())
#
#
#         # else:
#         #
#         #     client.send(bytes("{quit}", "utf8"))
#         #     client.close()
#         #     del clients[client]
#         #     broadcast(bytes("%s has left the chat." % name, "utf8"))
#         #     break
#
#
# def broadcast(msg, prefix=""):  # prefix is for name identification.
#     """Broadcasts a message to all the clients."""
#
#     for sock in clients:
#           sock.send(bytes(prefix, "utf8") + msg)
#
# clients = {}
# addresses = {}
#
# HOST = ''
# PORT = 9999
# BUFSIZ = 1024
# ADDR = (HOST, PORT)
#
# SERVER = socket(AF_INET, SOCK_STREAM)
# SERVER.bind(ADDR)
#
#
# if __name__ == "__main__":
#     ref = root.child("Data")
#     SERVER.listen(5)
#     print("Waiting for connection...")
#     ACCEPT_THREAD = Thread(target=accept_incoming_connections)
#     ACCEPT_THREAD.start()
#     ACCEPT_THREAD.join()
#     SERVER.close()

