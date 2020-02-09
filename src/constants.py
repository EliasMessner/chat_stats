
global_lang = "en"


# general_en

end_to_end_text_en = "Messages to this chat and calls are now secured with end-to-end encryption. Tap for more " \
                     "info."
end_to_end_text_group_en = "Messages to this group are now secured with end-to-end encryption. Tap for more info."
message_deleted_en = "This message was deleted"
you_deleted_message_en = "You deleted this message"
media_ommitted_en = "<Media omitted>"
missed_voice_call_en = "Missed voice call"
live_location_shared_en = "live location shared"
no_longer_admin_en = "You're no longer an admin"
now_admin_en = "You're now an admin"


# regexes_en

security_code_changed_en = r".* security code changed. Tap for more info"
switched_number_en = r".* switched to .*"
created_group_en = r".* created group .*"
changed_subject_en = r".* changed the subject .*to \".*\""
added_user_en = r".* added .*"
removed_user_en = r".* removed .*"
changed_group_description_en = r".* changed the group description"
changed_group_icon_en = r".* changed this group's icon"
deleted_group_icon_en = r".* deleted this group's icon"
left_en = r".* left"

message_separator_regex_en_android = r"\s(?=\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2})"
date_format_en = "%m/%d/%y, %I:%M %p"


# general_de

end_to_end_text_de = "Nachrichten, die du in diesem Chat sendest, sowie Anrufe, sind jetzt mit Ende-zu-Ende-Verschlüsselung geschützt. Tippe für mehr Infos."
end_to_end_text_group_de = "Nachrichten an diese Gruppe sind jetzt mit Ende-zu-Ende-Verschlüsselung geschützt. Tippe für mehr Infos."
message_deleted_de = "Diese Nachricht wurde gelöscht."
media_ommitted_de = "<Medien ausgeschlossen>"
missed_voice_call_de = "Verpasster Sprachanruf"
live_location_shared_de = "Live-Standort wird geteilt."
no_longer_admin_de = "Du bist kein Admin mehr."
now_admin_de = "Du bist jetzt ein Admin."


# regexes_de

security_code_changed_de = r"Die Sicherheitsnummer von .* hat sich geändert. Tippe für mehr Infos."
switched_number_de = r".* hat zu .* gewechselt."
created_group_de = r".* hat die Gruppe .* erstellt."
changed_subject_de = r".* hat den Betreff .*zu „.*“ geändert."
added_user_de = r".* hat .* hinzugefügt."
removed_user_de = r".* hat .* entfernt"
changed_group_description_de = r".* hat die Gruppenbeschreibung geändert."
changed_group_icon_de = r".* hat das Gruppenbild geändert."
deleted_group_icon_de = r".* hat das Gruppenbild gelöscht."
left_de = r".* hat die Gruppe verlassen."

message_separator_regex_de_android = r"\s(?=\d{2}.\d{2}.\d{2}, \d{2}:\d{2})"
date_format_de = "%d.%m.%y, %H:%M"


# numbers

conversation_max_message_time_in_minutes = 20
conversation_on_screen_max_message_time_in_minutes = 2


def general(lang: str = None):
    if lang is None:
        lang = global_lang
    if lang == "en":
        return [end_to_end_text_en,
                message_deleted_en,
                end_to_end_text_group_en,
                missed_voice_call_en,
                media_ommitted_en,
                live_location_shared_en,
                now_admin_en,
                no_longer_admin_en,
                you_deleted_message_en]
    if lang == "de":
        return [end_to_end_text_de,
                message_deleted_de,
                end_to_end_text_group_de,
                missed_voice_call_de,
                media_ommitted_de,
                live_location_shared_de,
                now_admin_de,
                no_longer_admin_de]


def regexes(lang:str = None):
    if lang is None:
        lang = global_lang
    if lang == "en":
        return [changed_subject_en,
                added_user_en,
                changed_group_description_en,
                left_en,
                deleted_group_icon_en,
                changed_group_icon_en,
                removed_user_en,
                created_group_en,
                switched_number_en,
                security_code_changed_en]
    if lang == "de":
        return [changed_subject_de,
                added_user_de,
                changed_group_description_de,
                left_de,
                deleted_group_icon_de,
                changed_group_icon_de,
                removed_user_de,
                created_group_de,
                switched_number_de,
                security_code_changed_de]


def get_message_separator(lang: str = None):
    if lang is None:
        lang = global_lang
    if lang == "en":
        return message_separator_regex_en_android
    if lang == "de":
        return message_separator_regex_de_android


def get_date_format(lang: str = None):
    if lang is None:
        lang = global_lang
    if lang == "en":
        return date_format_en
    if lang == "de":
        return date_format_de
