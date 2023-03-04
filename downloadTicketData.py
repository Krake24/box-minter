import json
import os
import requests

base_url = "https://www.champions.io/api/emperors-challenge"

print("To download all your ticket data, you'll need to find a certain String on the CA website. Instructions see TPS server.")
code = input("please enter that string here: ")
result=200
counter=1
while result >= 200 and result < 300:
    result = requests.get(f"{base_url}/exchange/{code}").status_code
    print(f"Metadata for {counter} box downloaded")
    counter = counter + 1

boxes = requests.get(f"{base_url}/find/{code}").json()

with open(os.path.dirname(os.path.realpath(__file__))+"/tickets.json", "w") as file:
    file.write(json.dumps(boxes))

