import json

import azure.functions as azf


def main(event: azf.GridEvent) -> str:
    result = json.dumps({
        'id': event.id,
        'data': event.get_json(),
        'topic': event.topic,
        'subject': event.subject,
        'event_type': event.event_type,
        'event_time': (event.insertion_time.isoformat()
                       if event.insertion_time else None),
    })

    return result
