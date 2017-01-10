import re

url_re = re.compile("(?:\s|^)<(https?://[\w./?+&+%$!#=\-_]+)>(?:\s|$)")
purge_re = re.compile("(purge) (\d+)")
list_re = re.compile("list")

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
    list_found = list_re.search(message)

    return list_found is not None


def purge_request(message):
    index_found = purge_re.search(message)

    if index_found is None:
        return None

    return int(index_found.group(2))
