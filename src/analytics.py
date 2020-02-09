# analyzes chats as sets of messages
# counts words, participants and other stats

from datetime import *
import re
import string
import itertools
from src.Message import Message
import src.constants as Constants
from src.message_handler import contains_hyperlink
from calendar import day_name


# averages

def get_average_word_count_per_message(message_list: list):
    total_word_count = len(extract_words(get_all_message_contents_as_string(message_list)))
    return total_word_count / len(message_list)


def get_average_word_count_per_day(message_list: list, user: str = None):
    """
    :param message_list: if user is specified, message list should be the entire list of messages in this chat,
        especially for group or in chats where the user has not participated from beginning to end
    :param user: optional, the user the average word count is wanted for.
        if not specified all users in this chat are taken in account
    :rtype: float
    """
    message_list_sorted_by_date = sorted(message_list, key=lambda x: x.date_time)
    days_texted = (message_list_sorted_by_date[-1].date_time - message_list_sorted_by_date[0].date_time).days + 1
    total_word_count = len(extract_words(get_all_message_contents_as_string(filter_messages(message_list, user))))
    return total_word_count / days_texted


def get_average_message_count_per_day(message_list: list, user: str = None):
    """
    :param message_list: if user is specified, message list should be the entire list of messages in this chat,
        especially for group or in chats where the user has not participated from beginning to end
    :param user: optional, the user the average message count is wanted for.
        if not specified all users in this chat are taken in account
    :rtype: float
    """
    message_list_sorted_by_date = sorted(message_list, key=lambda x: x.date_time)
    days_texted = (message_list_sorted_by_date[-1].date_time - message_list_sorted_by_date[0].date_time).days + 1
    return len(filter_messages(message_list, sender=user)) / days_texted


def get_average_word_length(message_list: list):
    return len(concatenate_list_data(extract_words(get_all_message_contents_as_string(message_list)))) \
           / len(extract_words(get_all_message_contents_as_string(message_list)))


def get_average_response_time(message_list: list, user: str):
    """
    :return: average response time in conversations in seconds
    :rtype: float
    """
    urd = get_user_response_dict(message_list)
    return urd[user][0] / urd[user][1]


# tops

def get_most_active_day(message_list: list):
    """
    :return: date on which most messages where sent
    :rtype: date
    """
    activity_date_dict = get_daily_activity(message_list)
    return max(activity_date_dict.keys(), key=lambda x: activity_date_dict[x])


def get_longest_message(message_list: list):
    return max(message_list, key=lambda x: len(x.content))


def get_longest_conversation_by_messages(message_list: list, allowed_minutes: int = None):
    """
    :param message_list: list of messages
    :type message_list: list
    :return: the longest conversation that took place (by number of messages sent).
    :rtype: list
    """
    return max(get_all_conversations(message_list, allowed_minutes), key=lambda x: len(x))


def get_longest_conversation_by_duration(message_list: list, allowed_minutes: int = None):
    """
    :return: the longest conversation that took place (by time difference from first to last message).
    :rtype: list
    """
    return max(get_all_conversations(message_list, allowed_minutes), key=lambda x: (max(x, key=lambda n: n.date_time).date_time
                                                                   - min(x, key=lambda m: m.date_time).date_time))


# totals

def get_all_participants(message_list: list):
    participants = []
    for msg in message_list:
        if msg.sender not in participants:
            participants.append(msg.sender)
    return participants


def get_all_message_contents_as_string(message_list: list):
    result = ""
    for msg in message_list:
        result = result + msg.content + " "
    return result


def filter_messages(message_list: list, sender=None, date_time_start: datetime = None,
                    date_time_stop: datetime = None, search: list = None):
    result = []
    for msg in message_list:
        if sender is not None and msg.sender != sender:
            continue
        if date_time_start is not None and msg.date_time < date_time_start:
            continue
        if date_time_stop is not None and msg.date_time > date_time_stop:
            continue
        if search is not None and not any(word in msg.content for word in search):
            continue
        result.append(msg)
    return result


def get_word_frequency(text: str, case_sensitive: bool = False, stop_after: int = None, sort: bool = True,
                       stop_words: list = None):
    """
    :return: dictionary with words as keys and their respective number of occurrences in given text as values
    :rtype: dict
    """
    if stop_words is None:
        stop_words = open(r"C:\Users\elias\PycharmProjects\wordCloudProject\resources\stopwords_de.txt", "r",
                          encoding="utf8").read().split("\n")
    if not case_sensitive:
        text = text.lower()
    freq_dict = {}
    words = extract_words(text, stop_words = stop_words)
    for word in words:
        if not word in freq_dict:
            freq_dict[word] = 1
        else:
            freq_dict[word] = freq_dict[word] + 1
    if sort:
        freq_dict = {k: v for k, v in sorted(freq_dict.items(), key=lambda item: item[1], reverse=True)}
    if stop_after is not None:
        freq_dict = dict(itertools.islice(freq_dict.items(), stop_after))
    return freq_dict


def extract_words(text: str, stop_words: list = None):
    """
    :param text: text to extract words from (keeps duplicates)
    :type text: str
    :param stop_words: words to ignore
    :type stop_words: list
    :return: list of words
    :rtype: list
    """
    if stop_words is None:
        stop_words = []
    text = re.sub("[^a-zA-ZßäöüÄÖÜ ]+","", text)
    words = re.sub('[' + string.punctuation + ']', '', text).split()
    filtered_words = []
    for w in words:
        if w in stop_words:
            continue
        filtered_words.append(w)
    return filtered_words


def get_daily_activity(message_list: list, exclude_non_active_days: bool = True):
    """
    :return: dict with all dates when messages where sent as keys, and the number of messages sent on each day as values
    :rtype: dict
    """
    result = {}
    for msg in message_list:
        if not msg.date_time.date() in result:
            result[msg.date_time.date()] = 1
        else:
            result[msg.date_time.date()] += 1
    if not exclude_non_active_days:
        # setting all non listed but within time frame days to 0
        current_day = min(result)
        while current_day <= max(result):
            if current_day not in result:
                result[current_day] = 0
            current_day += timedelta(days=1)
    return {k: v for k, v in sorted(result.items(), key=lambda item: item[0])}


def get_user_response_dict(message_list: list):
    """
    :return: dictionary with user as keys, values are 2 item lists with total response time in seconds as first and
    total responses as second item
    :rtype: dict
    """
    conversations = get_all_conversations(message_list)
    user_response_dict = {}  # {user, [total_response_time, number_of_responses]}
    for p in get_all_participants(message_list):
        user_response_dict[p] = [0, 0]
    for convo in conversations:
        message: Message
        previous_message = convo[0]
        for message in convo[1:]:  # first message is not a response but initiator
            if message.sender != previous_message.sender:
                response_time = (message.date_time - previous_message.date_time).seconds
                user_response_dict[message.sender] = [user_response_dict[message.sender][0] + response_time,
                                                      user_response_dict[message.sender][1] + 1]
            previous_message = message
    return user_response_dict


def get_message_count_on_day(message_list: list, day: date):
    count = 0
    for msg in message_list:
        if msg.date_time.date() == day:
            count += 1
    return count


def get_all_conversations(message_list: list, allowed_minutes: int = None):
    """
    :return: list of all conversations in this message list. A conversation is when a subsequent message has been sent within allowed_minutes
    :rtype: list[list]
    """
    result = []
    current_convo = []
    if allowed_minutes is None:
        allowed_minutes = Constants.conversation_max_message_time_in_minutes
    for msg in sorted(message_list, key=lambda x: x.date_time):
        if current_convo == [] or (msg.date_time - current_convo[-1].date_time).total_seconds() <= allowed_minutes * 60:
            current_convo.append(msg)
        else:
            if len(get_all_participants(current_convo)) > 1:
                result.append(current_convo)
            current_convo = []
    if current_convo != []:
        result.append(current_convo)
    return result


def get_participation_by_messages(message_list: list):
    """
    :return: users and their respective total amounts of messages contributed to the chat
    :rtype: dict
    """
    result = {}
    for msg in message_list:
        if msg.sender not in result:
            result[msg.sender] = 1
        else:
            result[msg.sender] += 1
    return result


def get_participation_by_words(message_list: list):
    """
    :return: users and their respective total amounts of words contributed to the chat
    :rtype: dict
    """
    result = {}
    for msg in message_list:
        if msg.sender not in result:
            result[msg.sender] = len(extract_words(msg.content))
        else:
            result[msg.sender] += len(extract_words(msg.content))
    return result


def get_participation_by_characters(message_list: list):
    """
    :return: users and their respective total amounts of characters contributed to the chat
    :rtype: dict
    """
    result = {}
    for msg in message_list:
        if msg.sender not in result:
            result[msg.sender] = len(msg.content)
        else:
            result[msg.sender] += len(msg.content)
    return result


def get_activity_per_week_day(message_list: list):
    """
    :return: dictionary with weekdays as keys and total number of messages sent on each day as keys
    :rtype: dict
    """
    result = {}
    for msg in message_list:
        weekday = day_name[msg.date_time.weekday()]
        if weekday not in result:
            result[weekday] = 1
        else:
            result[weekday] += 1
    return {k: v for k, v in sorted(result.items(), key=lambda item: list(day_name).index(item[0]))}


def get_activity_per_hour(message_list: list):
    """
    :return: dictionary with day-hours as keys and total number of messages sent in each hour as keys
    :rtype: dict
    """
    result = {}
    for msg in message_list:
        hour = msg.date_time.hour
        if hour not in result:
            result[hour] = 1
        else:
            result[hour] += 1
    return {k: v for k, v in sorted(result.items(), key=lambda item: item[0])}


def concatenate_list_data(given_list: list):
    result = ''
    for element in given_list:
        result += str(element)
    return result
