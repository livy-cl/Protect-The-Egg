def read_json(file_name: str) -> dict:
    from ujson import load
    with open(file_name) as json_file:
        json_dict = load(json_file)
        json_file.close()
    return json_dict
def write_json(file_name: str, data: object):
    from ujson import dump
    with open(file_name, "w+") as json_file:
        dump(data, json_file)
        json_file.close()
def read_file(file_name: str):
    with open(file_name) as text_file:
        file_content = text_file.read()
        text_file.close()
    return file_content
def time() -> int:
    from utime import mktime, localtime
    return mktime(localtime()) - read_json("data/dump")["startTime"]
def pretty_time() -> str:
    from math import fmod
    run_time_seconds = time()
    seconds = fmod(run_time_seconds, 60)
    minutes = int(run_time_seconds / 60)
    hours = int(minutes / 60)
    minutes = fmod(minutes, 60)
    days = int(hours / 60)
    hours = fmod(hours, 60)
    return "days:{days}, hr:{hours}, min:{minutes}, s:{seconds}".format(days=int(days), hours=int(hours),minutes=int(minutes), seconds=int(seconds))