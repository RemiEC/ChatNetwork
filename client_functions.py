'''
• Client function (command line):
#! 1) #Help (list command)
#! 2) #Exit (client exit)
#! 3) #ListU (list of users in a server)
#TODO Rémi 4) #ListF (list of files in a server)
#TODO Rémi 5) #TrfU (Upload file transfer to a server)
#TODO Rémi 6) #TrfD (transfer Download file to a server)
#TODO VALOT • # Private <user> (private chat with another user)
#TODO VALOT • #Public (back to the public)
#TODO MUTEZ 1) #Ring <user> (notification if the user is logged in)
#TODO MUTEZ Limit size of messages (280 characters)
2) Your original orders

'''

# Import sockets libraries
import socket
import select

# Import display library
from datetime import datetime


#! Commandes clients
EXIT_CLIENT = "#Exit" #Command used by clients to leave
HELP_CLIENT = "#Help" #Command used by clients to get help
LISTU_CLIENT = "#ListU" #Command used by clients to get the list of other connected users
PRIVATE_CLIENT = "#Private" #Command used by clients to chat privately with one another
PUBLIC_CLIENT = "#Public" #Command used by clients to get back to public chat after using private chat
CREATE_CHATROOM_CLIENT= "#CreateRoom" #Command used by clients to create group chats with multiple users
JOIN_CHATROOM_CLIENT="#JoinRoom"
LIST_CHATROOM_CLIENT="#ListRoom"
#TODO TOUJOURS mettre les 3 mêmes paramètres dans chaque fonction même si on ne se sert pas des 3
#TODO En effet les appels de fonctions sont définis par défaut avec ces paramètres dans la fonction Check_client_functions

def Client_Exit (client,msg_recu, clients_connectes, Rooms):
    if(msg_recu == EXIT_CLIENT):
        msg_client="'{}' left the chat".format(client.username)
        print("{} @{}:{} | '{}' has left the chat \n".format(datetime.now(), client.IP, client.port, client.username)) 

        for element in clients_connectes:
            if (client != element):
                element.socket.send(msg_client.encode())
        clients_connectes.remove(client)
        client.socket.close()
    
    else :
        raise Exception
        
def Client_Help (client,msg_recu, clients_connectes, Rooms):
    if(msg_recu == HELP_CLIENT):
        msg = "You can find a list of available commands below : \n \n \
        #Help (list command) \n \
        #Exit (exit chat) \n \
        #ListF (list of files in a server) \n \
        #ListU (list of users in a server) \n \
        #TrfU (Upload file transfer to a server) \n \
        #TrfD (transfer Download file to a server) \n \
        #Private <user> (private chat with another user) \n \
        #Public (back to the public chat) \n \
        #Ring <user> (notification if the user is logged in)\n \
        #CreateRoom <room name> (create private chat room with multiple clients) \n \
        #JoinRoom <room name> (Join a room the client was added to)\n \
        #ListRoom (List all rooms the client was added to)\n"

        client.socket.send(msg.encode())
    else:
        raise Exception

def Client_ListU (client,msg_recu, clients_connectes, Rooms):
    if(msg_recu == LISTU_CLIENT):
        msg=("\nList of users (except you of course): \n") 
        count_user=1

        for element in clients_connectes:
            if (client != element):
                msg+=("User {}: {} @{}:{}\n".format(count_user, element.username, element.IP, element.port))
                count_user+=1
        msg+="\n"
        client.socket.send(msg.encode())
    else :
        raise Exception

def Client_Private(client,msg_recu, clients_connectes, Rooms):
    client_connected_existed = False
    if(len(msg_recu.split(' ')) == 2): #on peut se permettre de verifier s'il n'y a que deux termes car le username ne peut pas contenir d'espace (regle qu'on a fixée)
        for other_client in clients_connectes:
            if (other_client.username == msg_recu.split(' ')[1]):
                client_connected_existed = True
                other_client.room=client.username
                client.room=other_client.username
                msg = "\nYou entered a private chat with '{}'.\n".format(client.username) 
                msg+="If you want to get back in the public chat, type '#Public'."
                other_client.socket.send(msg.encode())
                msg = "You entered a private chat with {}.\n".format(other_client.username) 
                msg+="If you want to get back in the public chat, type '#Public'."
                client.socket.send(msg.encode())
    
    if (len(msg_recu.split(' ')) == 1):
        client.socket.send(b"Please write a user's name after the command")

    if (client_connected_existed == False and len(msg_recu.split(' ')) != 1):
        client.socket.send(b"User not connected or not existing")


def Client_Public(client,msg_recu, clients_connectes, Rooms):
    if(msg_recu==PUBLIC_CLIENT):
        if(client.room != "public"):
            for other_client in clients_connectes:
                if(other_client.username==client.room):
                    msg="'{}' left the private chat.".format(client.username)
                    other_client.socket.send(msg.encode())
            client.room="public"
    else:
        raise Exception

def List_Room(client,msg_recu, clients_connectes):
    
    no_client=[]
    client_room=msg_recu.split(' ')[1:len(msg_recu.split(' '))]
    if(len(client_room) > 1): #on peut se permettre de verifier s'il n'y a que deux termes car le username ne peut pas contenir d'espace (regle qu'on a fixée)
        for i in range (len(client_room))
            client_connected_existed = False
            for other_client in clients_connectes:
                
                if (other_client.username == client_room[i]):
                    client_connected_existed = True
                    

            if(client_connected_existed==False):
                no_client.append(client_room[i])

    
    elif (len(client_room) == 0):
        client.socket.send(b"Please write a user's name after the command")
    
    elif (len(msg_recu.split(' ')) == 1):
        client.socket.send(b"Please write more than one user's name after the command, or use command #Private")
                       
def Create_Room(client,msg_recu, clients_connectes, Rooms):
    exist=False
    if(len(msg_recu.split(' '))>1):
        room_name = msg_recu.lstrip(msg_recu.split(' ')[0])
        room_name = room_name[1:len(room_name)]
        if(len(Rooms)!=0):
            for room in Rooms:
                if(room_name==room.name):
                    exist=True
                    break
        if(not exist):
            return client, room_name
    elif(len(msg_recu.split(' '))==1): 
        client.socket.send(b"Please precise a room name after the #CreateRoom command.")                    
    


options = {
        EXIT_CLIENT : Client_Exit,
        HELP_CLIENT : Client_Help,
        LISTU_CLIENT : Client_ListU,
        PRIVATE_CLIENT : Client_Private,
        PUBLIC_CLIENT : Client_Public,
        CREATE_CHATROOM_CLIENT : Create_Room,
        LIST_CHATROOM_CLIENT : List_Room
    }

def Check_client_functions(msg_recu, client, clients_connectes, Rooms):
    commande = msg_recu.split(' ')[0]

    try:
        return options[commande](client,msg_recu, clients_connectes, Rooms)
    except :
        msg = b"Command not found, try using #Help"
        client.socket.send(msg)
    

