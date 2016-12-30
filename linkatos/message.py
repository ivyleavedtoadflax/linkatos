import re

url_re = re.compile("(?:\s|^)<(https?://[\w./?+&+%$!#=\-_]+)>(?:\s|$)")

def extract_url(message):
    """
    Returns the first url in a message. If there aren't any returns None
    """
    answer = url_re.search(message)

    if answer is not None:
        answer = answer.group(1).strip()

    return answer


def to_bot(message, bot_id):
    bot_re = "^<@" + bot_id + '>'
    to_bot_re = re.compile(bot_re)
    bot_found = to_bot_re.search(message)

    return bot_found is not None


def is_list_request(message):
    list_re = re.compile("list")
    list_found = list_re.search(message)

    return list_found is not None
