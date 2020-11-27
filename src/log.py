from miscellaneous import time

debuggingState = True


def warning(warning_message: str):
    print("(" + str(time()) + ") WARNING: " + str(warning_message))


def error(error_message: str):
    print("(" + str(time()) + ") ERROR: " + str(error_message))


def message(log_message: str):
    print("(" + str(time()) + ") LOG: " + str(log_message))


def user_input(extra_message: str = ""):
    print("INPUT -> " + extra_message)
    return user_input()  # ask for user input


def debugging(debug_message: str):
    print("(" + str(time()) + ") DEBUGGING: " + str(debug_message))


def repeat_message(log_message: str, repeat: int, message_id: str = ""):
    from miscellaneous import read_json, write_json
    """
    print a message ones every [repeat] seconds and only one every second if you give the parameter
    repeat_message_previous_time

    :param log_message: the message
    :param repeat: how many seconds it takes to print the message again
    :param message_id: a id to get the previous time a repeat_message printed 
                       (so multiple repeat messages do not print in 1 second)
    :return: whether or not the message printed (printed = True)
    """
    json_dict = read_json("data/dump")

    if time() % repeat == 0 and not json_dict["repeatMessage"][message_id] == time():  # check if there is a rest when
        # you divide repeat by time() and if you already send a message of a certain id this second
        print("(" + str(time()) + ") LOG: " + str(log_message))  # print the message
        json_dict["repeatMessage"][message_id] = time()  # save time of message to json dictionary for next message/run

        write_json("data/dump", json_dict)  # save dictionary to the json file dump
