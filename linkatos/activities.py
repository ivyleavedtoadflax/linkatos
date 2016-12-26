import time
import linkatos.parser as parser
import linkatos.printer as printer
import linkatos.firebase as fb
import linkatos.reaction as react


def is_empty(events):
    return ((events is None) or (len(events) == 0))


def is_url(url_message):
    return url_message['type'] == 'url'


def event_consumer(expecting_url, expecting_reaction, parsed_url_message,
                   slack_client, fb_credentials, firebase):

    # Read slack events
    events = slack_client.rtm_read()
    time.sleep(1)  # 1 second delay after reading

    if is_empty(events):
        return (expecting_url, expecting_reaction, parsed_url_message)

    for event in events:
        print(event)
        print('expecting_url: ', expecting_url)

        if expecting_url and event['type'] == 'message':
            parsed_url_message = parser.parse_url_message(event)

            if is_url(parsed_url_message):
                printer.ask_confirmation(parsed_url_message, slack_client)
                expecting_url = False

        if not expecting_url and event['type'] == 'reaction_added':
            reaction = parser.parse_reaction_added(event)

            if react.is_confirmation(reaction['reaction'],
                                     parsed_url_message['id'],
                                     reaction['to_id']):
                react.handle(reaction['reaction'], parsed_url_message['url'],
                             fb_credentials, firebase)
                expecting_url = True

    return (expecting_url, expecting_reaction, parsed_url_message)
