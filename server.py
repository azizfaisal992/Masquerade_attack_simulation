import socket
import json
from pathlib import Path

ACCOUNTS_FILE = Path(__file__).with_name("accounts.json")
HOST = "127.0.0.1"
PORT = 5001

def load_accounts():
    with ACCOUNTS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)

def send_json(conn, data):
    message = json.dumps(data) + "\n"
    conn.sendall(message.encode("utf-8"))


def handle_client(conn,accounts):
    file = conn.makefile("r", encoding="utf-8")

    for line in file:
        try:
            request = json.loads(line)
            action = request.get("action")

            if action == "login":
                username = request.get("username")
                password = request.get("password")
                account = accounts.get(username)

                if account and account["password"] == password:
                    send_json(conn, {
                        "status": "OK",
                        "message": "LOGIN SUCCESSFULLY",
                        "username": username,
                        "balance": account["balance"]
                    })
                else:
                    send_json(conn, {
                        "status": "error",
                        "message": "invalid username & password"
                    })

            elif action == "check_balance":
                username = request.get("username")
                account = accounts.get(username)

                if account:
                    send_json(conn, {
                        "status": "ok",
                        "username": username,
                        "balance": account["balance"]
                    })
                else:
                    send_json(conn, {
                        "status": "error",
                        "message": "account not found"
                    })

            else:
                send_json(conn, {
                    "status": "error",
                    "message": "unknown action"
                })

        except json.JSONDecodeError:
            send_json(conn,{
                "status": "error",
                "message": "Invalid json"
            })

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

    server.bind((HOST,PORT))

    server.listen()

    accounts = load_accounts()
    print(f"loaded {len(accounts)}")

    print(f"MINI BANK SERVER STARTING... {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()

        with conn:
            print("client connected")
            handle_client(conn,accounts)

if __name__ == "__main__":
    start_server()