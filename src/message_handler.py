from src.Message import Message
import re, datetime
import src.constants as constants
import emoji
from src.analytics import *
from collections import Counter


def get_all_messages(path: str, stop_after: int = None, separator_regex: str = None, date_format: str = None,
                     exclude_hyperlinks: bool = True):
    if separator_regex is None:
        separator_regex = constants.get_message_separator()
    if date_format is None:
        date_format = constants.get_date_format()
    result = []
    file = open(path, "r", encoding="utf8")
    file_string = file.read()
    count = 0
    for raw_message_as_string in split_by_messages(separator_regex, file_string):
        if any(text in raw_message_as_string for text in constants.general()) \
                or any(re.search(pattern, raw_message_as_string) for pattern in constants.regexes()) \
                or (exclude_hyperlinks and contains_hyperlink(raw_message_as_string)):
            continue
        try:
            result.append(parse_message(raw_message_as_string, separator_regex, date_format))
        except ValueError:
            print("failed to parse message(skipped):", raw_message_as_string)
            pass
        except Exception:
            print("failed to parse message:", raw_message_as_string)
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
    date_time = datetime.strptime(date_string, date_format)
    return Message(date_time, sender, content)


def contains_hyperlink(string: str):
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+] | [! * \(\),] | (?: %[0-9a-fA-F][0-9a-fA-F]))+', string)
    return len(url) != 0


# some tests:

if __name__ == "__main__":
    messages = get_all_messages(r"C:\Users\elias\Desktop\WA chats\WhatsApp Chat with S.txt")
    for m in messages:
        print(str(m)+"\n\n")
    print(str(len(messages))+" Messages parsed.")

    el = extract_emojis(get_all_message_contents_as_string(messages))
    print("\nEmojis:", el)
    print(count_emojis(el))
    print(emoji.EMOJI_UNICODE)