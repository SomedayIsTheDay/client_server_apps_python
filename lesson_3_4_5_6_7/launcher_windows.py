import subprocess
from time import sleep

PROCESS = []

while True:
    ACTION = input(
        "Choose one option: q - quit, "
        "s - turn on the server and the clients, x - turn off everything: "
    )

    if ACTION == "q":
        break
    elif ACTION == "s":
        PROCESS.append(
            subprocess.Popen(
                "python server.py", creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        )
        for i in range(2):
            sleep(0.5)
            PROCESS.append(
                subprocess.Popen(
                    "python client.py -o send",
                    creationflags=subprocess.CREATE_NEW_CONSOLE,
                )
            )
        for i in range(5):
            sleep(0.5)
            PROCESS.append(
                subprocess.Popen(
                    "python client.py -o listen",
                    creationflags=subprocess.CREATE_NEW_CONSOLE,
                )
            )
    elif ACTION == "x":
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()
