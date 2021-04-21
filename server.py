import os

from fastapi import FastAPI
import ujson as json
import subprocess

import uvicorn

app = FastAPI()


@app.get("/")
def fun():
    return "This is a root"


@app.get("/get")
def open_json():
    with open("top_score.json", "r") as file:
        return {k: int(v) for k, v in sorted(json.load(file).items(), key=lambda item: item[1])[::-1]}


@app.get("/write")
def write_to_json(data: str):
    dictionary = {**open_json(), **eval(data)}
    with open('top_score.json', 'w') as file:
        json.dump(dictionary, file, indent=4, ensure_ascii=False)
    return "Complete"


@app.get("/delete")
def write_to_json(data: str):
    dictionary = open_json()
    try:
        del dictionary[data]
        with open('top_score.json', 'w') as file:
            json.dump(dictionary, file, indent=4, ensure_ascii=False)
        return "Complete"
    except Exception as e:
        return e


@app.get("/reboot")
def reboot_server():
    try:
        os.system("shutdown /r /t 1")
        # subprocess.check_call('reboot')
        # subprocess.check_call(['systemctl', 'reboot', '-i'])
        return "Rebooting..."
    except Exception as e:
        return e


def run_server():
    uvicorn.run(app, host="0.0.0.0", port=49150)


run_server()
