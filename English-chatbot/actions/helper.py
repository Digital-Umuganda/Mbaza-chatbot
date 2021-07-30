from typing import Dict, Text, Any, Optional, List
from rasa_sdk import Tracker

import json


def get_entity_details(
    tracker: Tracker, entity_type: Text
) -> Optional[Dict[Text, Any]]:
    all_entities = tracker.latest_message.get("entities", [])
    entities = [e for e in all_entities if e.get("entity") == entity_type]
    if entities:
        return entities[0]


def detect_entity(
    tracker: Tracker, entity_types: List[str]
) -> Optional[Dict[Text, Any]]:
    all_entities = tracker.latest_message.get("entities", [])

    for e in all_entities:
        for e_type in entity_types:
            if e.get("entity") == e_type:
                return e_type


def intent_to_message(intent: str) -> Optional[str]:
    filename = "data/utils/intent_mapping.json"
    with open(filename) as data:
        intent_mapping = json.load(data)

        for item, message in intent_mapping.items():
            if item == intent:
                return message


def lockdown_lookup(location):
    filename = "data/utils/lockdown.json"
    with open(filename) as data:
        lockdown_status = json.load(data)

        for item, status in lockdown_status.items():
            if item == location:
                return status
