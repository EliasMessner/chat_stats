from src.visualization import *
from src.message_handler import *
from src.analytics import *
import src.constants as constants


def main():

    # chat_path = r"C:\Users\elias\Desktop\WA chats\fam_group.txt"
    chat_path = r"C:\Users\elias\Desktop\WA chats\WhatsApp Chat with S.txt"
    # chat_path = r"C:\Users\elias\Desktop\WA chats\groupChat.txt"
    # chat_path = r"C:\Users\elias\Desktop\WA chats\groupChat_full_de.txt"
    # chat_path = r"C:\Users\elias\Desktop\WA chats\WhatsApp Chat with Sis.txt"
    # chat_path = r"C:\Users\elias\Downloads\WhatsApp Chat with Rick Justin Junge.txt"

    # Constants.global_lang = "de"

    stopwords_de = open(r"C:\Users\elias\PycharmProjects\wordCloudProject\resources\stopwords_de.txt", "r",
                        encoding="utf8").read().split("\n")
    print(str(len(stopwords_de)) + " stopwords.")

    mask_path = r"C:\Users\elias\PycharmProjects\wordCloudProject\resources\whatsapp_logo.png"

    all_messages = get_all_messages(chat_path)
    participants = get_all_participants(all_messages)

    for p in participants:
        filtered_messages = filter_messages(all_messages, sender=p)
        print("\n\n\n\nStats for " + p + ":\n")
        print("\nTotal messages sent: ", len(filtered_messages))
        print("\nTotal words typed: ", len(extract_words(get_all_message_contents_as_string(filtered_messages))))
        print("\nTotal chars typed (incl spaces): "
              + str(len(get_all_message_contents_as_string(filtered_messages))))
        print("\nAverage words per message: %.2f" % get_average_word_count_per_message(filtered_messages))
        print("\nAverage messages per day:  %.2f" % get_average_message_count_per_day(all_messages, p))
        print("\nAverage word length:  %.2f" % get_average_word_length(filtered_messages))
        # print("\nlongest message:\n", get_longest_message(filtered_messages).date_time, "\n", len(get_longest_message(filtered_messages).content), "characters, ", len(extract_words(get_longest_message(filtered_messages).content)), "words")
        print("\nlongest message:\n", get_longest_message((filtered_messages)))
        most_active_day = get_most_active_day(filtered_messages)
        print("\nmost active day:\n", most_active_day,
              "\nmessages sent on this day:", get_message_count_on_day(filtered_messages, most_active_day))

        print("\nFavorite word:",
              get_word_frequency(get_all_message_contents_as_string(filtered_messages), stop_after=1, stop_words=[]))
        print("\nFavorite word (without stop words):",
              get_word_frequency(get_all_message_contents_as_string(filtered_messages), stop_after=1))
        print("\nAverage response time (minutes): %.2f" % (get_average_response_time(all_messages, user=p)/60))

        # plot_word_cloud(get_all_message_contents_as_string(filtered_messages), stopwords=stopwords_de, mask_path=None, caption="Word Cloud: " + p)
        # plot_barh_dict(get_word_frequency(get_all_message_contents_as_string(filtered_messages), stop_after=15), caption="Favorite words of " + p)
        # plot_barh_dict(get_word_frequency(get_all_message_contents_as_string(filtered_messages), stop_after=15, stop_words=[]), caption="Favorite words of " + p + " (incl stop words)")

    print("\n\n\nTogether stats: ")
    print("\nTotal messages sent:", len(all_messages))
    print("\nTotal words typed:", len(extract_words(get_all_message_contents_as_string(all_messages))))
    print("\nTotal chars typed (incl spaces): ", len(get_all_message_contents_as_string(all_messages)))
    print("\nAverage words per message: %.2f" % get_average_word_count_per_message(all_messages))
    print("\nAverage messages per day:  %.2f" % get_average_message_count_per_day(all_messages))
    print("\nAverage word length:  %.2f" % get_average_word_length(all_messages))
    # print("\nlongest message:\nby",get_longest_message(all_messages).sender,"\n", len(get_longest_message(all_messages).content), "characters, ",len(extract_words(get_longest_message(all_messages).content))," words")
    print("\nlongest message:\n", get_longest_message((all_messages)))
    most_active_day = get_most_active_day(all_messages)
    print("\nmost active day:\n", most_active_day,
          "\nmessages sent on this day: ", get_message_count_on_day(all_messages, most_active_day))

    print("\n\nNumber of conversations (Conversation means a subsequent message was sent within ",
          constants.conversation_max_message_time_in_minutes, " minutes): ",
          len(get_all_conversations(all_messages)))

    longest_convo_by_time = get_longest_conversation_by_duration(all_messages)
    print("\nlongest conversation by time:"
          "\n    from ", longest_convo_by_time[0].date_time,
          "\n    to ", longest_convo_by_time[-1].date_time,
          "\n(", (longest_convo_by_time[-1].date_time - longest_convo_by_time[0].date_time).total_seconds() / 60,
          " minutes)",
          "\n    messages: ", (len(longest_convo_by_time)))

    longest_convo_by_messages = get_longest_conversation_by_messages(all_messages)
    print("\nlongest conversation by number of messages exchanged:"
          "\n    from ", longest_convo_by_messages[0].date_time,
          "\n    to ", longest_convo_by_messages[-1].date_time,
          "\n(", (longest_convo_by_messages[-1].date_time - longest_convo_by_messages[0].date_time).total_seconds() / 60,
          " minutes)",
          "\n    messages: ", (len(longest_convo_by_messages)))

    print("\n\nNumber of on-screen-conversations (on-screen-conversation means a subsequent message was sent within ",
          constants.conversation_on_screen_max_message_time_in_minutes, " minutes): ",
          len(get_all_conversations(all_messages, allowed_minutes=constants.conversation_on_screen_max_message_time_in_minutes)))

    longest_convo_by_time = get_longest_conversation_by_duration(all_messages, allowed_minutes=constants.conversation_on_screen_max_message_time_in_minutes)
    print("\nlongest on-screen-conversation by time:"
          "\n    from ", longest_convo_by_time[0].date_time,
          "\n    to ", longest_convo_by_time[-1].date_time,
          "\n(", (longest_convo_by_time[-1].date_time - longest_convo_by_time[0].date_time).total_seconds() / 60,
          " minutes)",
          "\n    messages: ", (len(longest_convo_by_time)))

    longest_convo_by_messages = get_longest_conversation_by_messages(all_messages, allowed_minutes=constants.conversation_on_screen_max_message_time_in_minutes)
    print("\nlongest on-screen-conversation by number of messages exchanged:"
          "\n    from ", longest_convo_by_messages[0].date_time,
          "\n    to ", longest_convo_by_messages[-1].date_time,
          "\n(",
          (longest_convo_by_messages[-1].date_time - longest_convo_by_messages[0].date_time).total_seconds() / 60,
          " minutes)",
          "\n    messages: ", (len(longest_convo_by_messages)))

    '''
    plot_word_cloud(get_all_message_contents_as_string(all_messages), stopwords=stopwords_de, mask_path=mask_path, caption="Word Cloud")
    plot_barv_dict(get_daily_activity(all_messages, exclude_non_active_days=False), xtick_number=10)
    plot_pie_chart(get_participation_by_messages(all_messages), caption="Participation by messages")
    plot_pie_chart(get_participation_by_words(all_messages), caption="Participation by words")
    plot_pie_chart(get_participation_by_characters(all_messages), caption="Participation by characters")
    plot_barv_dict(get_activity_per_week_day(all_messages), caption="Activity per weekday")
    plot_barv_dict(get_activity_per_hour(all_messages), caption="Activity per hour")
    '''
    plt.show()


if __name__ == "__main__":
    main()
