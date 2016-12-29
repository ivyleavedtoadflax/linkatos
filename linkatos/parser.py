from . import message


def parse_url_message(event):
    url = message.extract_url(event['text'])

    if url is None:
        return None

    url_cache = {
        'url': url,
        'channel': event['channel'],
        'id': event['ts'],
        'type': 'url',
        'user': event['user']
    }

    return url_cache


def parse_reaction_added(event):
    reaction = {
        'reaction': event['reaction'],
        'channel': event['item']['channel'],
        'to_id': event['item']['ts'],
        'type': 'reaction',
        'user': event['user'],
        'to_user': event['item_user']
    }

    return reaction


def parse_linkatos_message(event):
    message = message.extract_list(event['text'])

    if message is None:
        return None

    linkatos_message = {
        'message' = message,
        'channel' = event['channel'],
        'type' = 'list'
    }

    return linkatos_message
