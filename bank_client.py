import socket
import json
HOST = "127.0.0.1"
PORT = 5001

def send_json(conn, data):
    message = json.dumps(data) + "\n"
    conn.sendall(message.encode("utf-8"))


def receive_json(file):
    line = file.readline()

    return json.loads(line)



def main():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST,PORT))

        print ("Connectd to bank server")

        file = client.makefile("r", encoding="utf-8")
        username = input("Username: ")
        password = input("Password: ")

        send_json(client, {
            "action":"login",
            "username": username,
            "password" : password,

        })
        response = receive_json(file)
        if response["status"] == "OK":
            print("login successful")
            print("ACCOUNT HOLDER: ", response["username"])
            print("Balance: ", response["balance"], "BDT")
        else:
            print("LOGIN FAILED: " ,response["message"])


    except ConnectionRefusedError:
        print("Connected refused. Start server.py again or first")

if __name__ == "__main__":
    main()
