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
    from miscellaneous import read_json, write_json, time
    json_dict = read_json("data/dump")
    if time() % repeat == 0 and not json_dict["repeatMessage"][message_id] == time():
        print('\033[92m' + "(" + str(pretty_time()) + ") LOG: " + str(log_message) + '\033[0m')
        json_dict["repeatMessage"][message_id] = time()
        write_json("data/dump", json_dict)
