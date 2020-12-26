def read_json(file_name: str) -> dict:
    """
    read a json file

    :param file_name: the name of the json file
    :return: the content of the json file
    """
    from ujson import load

    with open(file_name) as json_file:
        json_dict = load(json_file)
        json_file.close()

    return json_dict


def write_json(file_name: str, data: object):
    """
    write (or/and create) to a json file

    :param file_name: the name of the json file
    :param data: what you want to write
    """
    from ujson import dump

    with open(file_name, "w+") as json_file:
        dump(data, json_file)
        json_file.close()


def read_file(file_name: str):
    """
        read a text file (doesn't need to be .txt)

        :param file_name: the name of the json file
        :return: the content of the file
        """

    with open(file_name) as text_file:
        file_content = text_file.read()
        text_file.close()

    return file_content


def write_text_file(file_name: str, data: str):
    """
    write to a text file (doesn't need to be .txt) this will delete all the content of the file and replace it with your
    data/content

    :param file_name: the name of the text file
    :param data: what you want to write
    """

    with open(file_name, "w+") as text_file:
        text_file(str(file_name), str(data))
        text_file.close()


def append_text_file(file_name: str, data: str):
    """
    append to a text file (doesn't need to be .txt) this will add the data string to the and of the file

    :param file_name: the name of the text file
    :param data: what you want add to the file
    """

    with open(file_name, "a+") as text_file:
        text_file(str(file_name), str(data))
        text_file.close()


def time() -> int:
    """
    Returns: amount of seconds from boot
    """
    from utime import mktime, localtime
    return mktime(localtime()) - read_json("data/dump")["startTime"]


def pretty_time() -> str:
    import math

    run_time_seconds = time()
    seconds = math.fmod(run_time_seconds, 60)
    minutes = int(run_time_seconds/60)
    hours = int(minutes/60)
    minutes = math.fmod(minutes, 60)
    days = int(hours/60)
    hours = math.fmod(hours, 60)

    return "days:{days}, hr:{hours}, min:{minutes}, s:{seconds}".format(days=int(days), hours=int(hours), minutes=int(minutes), seconds=int(seconds))
