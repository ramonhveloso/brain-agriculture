from datetime import datetime


def add_timestamp(_, __, event_dict):
    event_dict["timestamp"] = datetime.now().isoformat()
    return event_dict


def rename_event_key(_, __, event_dict):
    if "event" in event_dict:
        event_dict["message"] = event_dict.pop("event")
    return event_dict


def remove_exc_info(_, __, event_dict):
    if event_dict.get("exc_info") is None:
        event_dict.pop("exc_info", None)
    return event_dict
