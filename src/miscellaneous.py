def read_json(file_name: str) -> dict:
    """
    read a json file

    :param file_name: the name of the json file
    :return: the content of the json file
    """
    from ujson import load

    with open(file_name) as json_file:  # open the file
        json_dict = load(json_file)  # load the content
        json_file.close()  # close the file
    return json_dict  # exit with the content


def write_json(file_name: str, data: object):
    """
    write (or/and create) to a json file

    :param file_name: the name of the json file
    :param data: what you want to write
    """
    from ujson import dump

    with open(file_name, "w+") as json_file:  # open the file or create the file if it does not exist
        dump(data, json_file)  # put the data in the file
        json_file.close()  # close the file


def read_file(file_name: str):
    """
    read a text file (doesn't need to be .txt)

    :param file_name: the name of the json file
    :return: the content of the file
    """
    with open(file_name) as text_file:  # open the file
        file_content = text_file.read()  # read the content of the file
        text_file.close()  # close the file

    return file_content  # Return with the content


def time() -> int:
    """
    Returns: amount of seconds from boot
    """
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

    return "days:{days}, hr:{hours}, min:{minutes}, s:{seconds}".format(days=int(days), hours=int(hours),
                                                                        minutes=int(minutes), seconds=int(seconds))
