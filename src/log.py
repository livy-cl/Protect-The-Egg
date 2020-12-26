"""
The code in the beginning of all the print statements (e.g. '\033[93m' ) is to give it color.
"""

from miscellaneous import pretty_time

debuggingState = True


def warning(warning_message: str):
    print('\033[93m' + "(" + str(pretty_time()) + ") WARNING: " + str(warning_message) + '\033[0m')


def error(error_message: str):
    print('\033[91m' + "(" + str(pretty_time()) + ") ERROR: " + str(error_message) + '\033[0m')


def message(log_message: str):
    print('\033[92m' + "(" + str(pretty_time()) + ") LOG: " + str(log_message) + '\033[0m')


def debugging(debug_message: str):
    if debuggingState:
        print('\033[0m' + "(" + str(pretty_time()) + ") DEBUGGING: " + str(debug_message) + '\033[0m')


def repeat_message(log_message: str, repeat: int, message_id: str = ""):
    """
    print a message ones every [repeat] seconds and only one every second if you give the parameter
    repeat_message_previous_time

    :param log_message: the message
    :param repeat: how many seconds it takes to print the message again
    :param message_id: a id to get the previous time a repeat_message printed 
                       (so multiple repeat messages do not print in 1 second)
    :return: whether or not the message printed (printed = True)
    """
    from miscellaneous import read_json, write_json, time
    json_dict = read_json("data/dump")

    if time() % repeat == 0 and not json_dict["repeatMessage"][message_id] == time():  # check if there is a rest when
        # you divide repeat by time() and if you already send a message of a certain id this second
        print('\033[92m' + "(" + str(pretty_time()) + ") LOG: " + str(log_message) + '\033[0m')  # print the message
        json_dict["repeatMessage"][message_id] = time()  # save time of message to json dictionary for next message/run

        write_json("data/dump", json_dict)  # save dictionary to the json file dump
