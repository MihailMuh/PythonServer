import threading
from fastapi import FastAPI
import ujson as json
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
def delete_from_json(data: str):
    dictionary = open_json()
    try:
        del dictionary[data]
        with open('top_score.json', 'w') as file:
            json.dump(dictionary, file, indent=4, ensure_ascii=False)
        return "Complete"
    except Exception as e:
        return e


@app.get("/filter")
def filter_top():
    dictionary_now = open_json()
    with open('last_top.json', 'r') as file:
        dictionary_last = {k: int(v) for k, v in sorted(json.load(file).items(), key=lambda item: item[1])[::-1]}

    dictionary = dictionary_now.copy()
    for i in dictionary_now:
        for j in dictionary_last:
            if (i == j) and (dictionary_now.get(i) == dictionary_last.get(j)):
                print(i, j, dictionary_now.get(i))
                del dictionary[i]

    with open('top_score.json', 'w') as file:
        json.dump(dictionary, file, indent=4, ensure_ascii=False)
    return "Complete"


@app.get("/make_finger")
def make_top_finger():
    with open('last_top.json', 'w') as file:
        json.dump(open_json(), file, indent=4, ensure_ascii=False)
    return "Complete"


@app.get("/make_filter")
def make_filter():
    filter_top()
    make_top_finger()

    threading.Timer(2678400, make_filter).start()


def run_server():
    uvicorn.run(app, host="0.0.0.0", port=49150)


make_filter()
run_server()
