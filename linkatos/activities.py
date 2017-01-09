from . import parser
from . import printer
from . import firebase as fb
from . import reaction as react
from . import message


def is_empty(events):
"""
Checks if a batch of Slack events is `None` or has zero elements.
"""
    return ((events is None) or (len(events) == 0))


def is_url(element):
"""
Checks if the input is not `None`.
The input is supposed to be a Slack event, but that's currently not verified.
"""
    return element is not None


def is_not_from_bot(bot_id, user_id):
"""
Compares two bot ids verifies they're different.
"""
    return not bot_id == user_id


def is_empty_list(xs):
"""
Checks if a list is empty.
"""
    return len(xs) == 0


def is_unfurled(event):
"""
Checks if a Slack event comes from unfurling a url.

          Currently assumes that any such message can be identified by the fact that it
          contains a _'previous_message'_ field.
"""
    return 'previous_message' in event


def event_consumer(cache, slack_client, bot_id, fb_credentials, firebase):
"""
Consumes batches of slack events and runs the possible actions.

Reads new batches of Slack events.
Selects those events that need to be actioned.
Actions events that:

    - are of 'type' _message_ and
        + contain a url
        + and caches the url
        + request a list of the cache
        + and prints out the list

    or

    - are of 'type' _reaction_added_ to a cached url
        + and either stores
        + or ignores the url
...

"""
    # Read slack events
    events = slack_client.rtm_read()

    if is_empty(events):
        return cache

    for event in events:
        if is_unfurled(event):
            return cache

        if event['type'] == 'message' and 'username' not in event:
            new_url = parser.parse_url_message(event)

            if is_url(new_url) and is_not_from_bot(bot_id, new_url['user']):
                cache.append(new_url)
                printer.ask_confirmation(new_url, slack_client)
                return cache

            if message.to_bot(event['text'], bot_id):
                list_request = parser.parse_list_request(event)
                purge_request = parser.parse_purge_request(event)

                if list_request is not None and list_request['type'] == 'list_request':
                    printer.list_cache(cache,
                                       list_request['channel'],
                                       slack_client)
                    return cache

                if purge_request is not None and \
                   purge_request['type'] == 'purge_request' and \
                   not is_empty_list(cache):
                    react.extract_url_by_index(cache,
                                               purge_request['index'] - 1)
                    printer.list_cached(cache,
                                        purge_request['channel'],
                                        slack_client)
                    return cache

        if event['type'] == 'reaction_added' and len(cache) > 0:
            reaction = parser.parse_reaction_added(event)

            if react.is_known(reaction['reaction']):
                selected_url = react.extract_url_by_id(cache,
                                                       reaction['to_id'])
                react.handle(reaction['reaction'], selected_url['url'],
                             fb_credentials, firebase)
                return cache

    return cache
