from src.Message import Message
import re, datetime
import src.constants as Constants


def get_all_messages(path: str, stop_after: int = None, separator_regex: str = None, date_format: str = None,
                     exclude_hyperlinks: bool = True):
    if separator_regex is None:
        separator_regex = Constants.get_message_separator()
    if date_format is None:
        date_format = Constants.get_date_format()
    result = []
    file = open(path, "r", encoding="utf8")
    file_string = file.read()
    count = 0
    for message_as_string in split_by_messages(separator_regex, file_string):
        if any(text in message_as_string for text in Constants.general()) \
                or any(re.search(pattern, message_as_string) for pattern in Constants.regexes()) \
                or (exclude_hyperlinks and contains_hyperlink(message_as_string)):
            continue
        try:
            result.append(parse_message(message_as_string, separator_regex, date_format))
        except ValueError:
            print("failed message(skipped): " + message_as_string)
            raise
        except Exception:
            print("failed message: "+message_as_string)
            raise
        count += 1
        if stop_after is not None and count > stop_after:
            break
    return result


def split_by_messages(separator_regex: str, file_string: str):
    return re.split(separator_regex, file_string)


def parse_message(message_as_string: str, regex: str, date_format: str):
    date_string, rest = message_as_string.split(" - ", 1)
    sender, content = rest.split(": ", 1)
    date_time = datetime.datetime.strptime(date_string, date_format)
    return Message(date_time, sender, content)


def contains_hyperlink(string: str):
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+] | [! * \(\),] | (?: %[0-9a-fA-F][0-9a-fA-F]))+', string)
    return len(url) != 0


# some tests:

if __name__ == "__main__":
    messages = get_all_messages(r"C:\Users\elias\PycharmProjects\wordCloudProject\resources\testChat.txt")
    for m in messages:
        print(str(m)+"\n\n")
    print(str(len(messages))+" Messages parsed.")