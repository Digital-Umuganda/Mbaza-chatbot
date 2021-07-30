# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from os import stat
import requests
from requests.exceptions import HTTPError

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType, ActionExecuted, UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher

from actions.helper import (
    get_entity_details,
    detect_entity,
    intent_to_message,
    lockdown_lookup,
)

#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


class ActionCheckStatistics(Action):
    """Check country covid statistics"""

    def name(self) -> Text:
        return "action_check_statistics"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        location = get_entity_details(tracker, "GPE")
        if location:
            location = location.get("value").lower()
        else:
            location = "rwanda"

        try:
            url = (
                "https://disease.sh/v3/covid-19/all"
                if location == "world"
                else "https://disease.sh/v3/covid-19/countries/" + location
            )
            res = requests.get(url)
            jsonResult = res.json()
            todayCases = str(jsonResult["todayCases"])
            totalCases = str(jsonResult["cases"])

            responseVars = {
                "number": todayCases,
                "location": location.capitalize(),
                "total": totalCases,
            }

            dispatcher.utter_message(response="utter_statistics", **responseVars)
            dispatcher.utter_message(response="utter_did_that_help")

        except HTTPError as httpError:
            dispatcher.utter_message(f"HTTP error occurred: {httpError}")
        except Exception as err:
            dispatcher.utter_message(f"Other error occurred: {err}")

        return []


class ActionShowTestingCenters(Action):
    """Display covid testing centers"""

    def name(self) -> Text:
        return "action_show_testing_centers"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        location = get_entity_details(tracker, "location")
        print("location===", location)
        if location:
            location = location.get("value").lower()
            if location == "kigali":
                dispatcher.utter_message(response="utter_show_kigali_testing_centers")
            else:
                dispatcher.utter_message(response="utter_show_other_testing_centers")

        else:
            dispatcher.utter_message(response="utter_within_or_outside_kigali")

        return []


class ActionCheckFinesPenalties(Action):
    """Display covid fines and penalties"""

    def name(self) -> Text:
        return "action_check_fines_penalties"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        entity_types = [
            "offence-mask",
            "offence-distance",
            "offence-curfew",
            "offence-gathering",
            "offence-lockdown",
            "offence-bar",
        ]

        entity = detect_entity(tracker, entity_types)
        print("entity===", entity)
        if entity:
            if entity == "offence-mask":
                dispatcher.utter_message(response="utter_fines_penalties_mask")
            elif entity == "offence-distance":
                dispatcher.utter_message(response="utter_fines_penalties_distance")
            elif entity == "offence-curfew":
                dispatcher.utter_message(response="utter_fines_penalties_curfew")
            elif entity == "offence-gathering":
                dispatcher.utter_message(response="utter_fines_penalties_gathering")
            elif entity == "offence-lockdown":
                dispatcher.utter_message(response="utter_fines_penalties_lockdown")
            elif entity == "offence-bar":
                dispatcher.utter_message(response="utter_fines_penalties_bar")
            else:
                dispatcher.utter_message("None of the related entity extracted")
        else:
            dispatcher.utter_message(response="utter_choose_fines_penalties")

        return []


class ActionDefaultAskAffirmation(Action):
    """ Overwriting default implementation which asks the user to affirm his intent."""

    def name(self) -> Text:
        return "action_default_ask_affirmation"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        """Runs action. Please see parent class for the full docstring."""
        intent_to_affirm = tracker.latest_message["intent"].get("name")

        intent_ranking = tracker.latest_message.get("intent_ranking", [])
        if intent_to_affirm == "nlu_fallback" and len(intent_ranking) > 1:
            intent_to_affirm = intent_ranking[1]["name"]

        affirmation_message = f"Did you mean {intent_to_message(intent_to_affirm)}?"
        affirmation_buttons = [
            {"title": "Yes", "payload": f"/{intent_to_affirm}"},
            {"title": "No", "payload": "/out_of_scope"},
        ]

        dispatcher.utter_message(text=affirmation_message, buttons=affirmation_buttons)

        return []


class ActionCheckLockdown(Action):
    """Display if a location is under lockown or not"""

    def name(self) -> Text:
        return "action_check_lockdown"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        location = get_entity_details(tracker, "location")
        if location:
            location = location.get("value").capitalize()
            status = lockdown_lookup(location)
            isOrIsNot = "is"

            print("loc===", location)
            print("status===", status)

            if status:
                if status == "no":
                    isOrIsNot = "is not"
            else:
                dispatcher.utter_message(
                    response="utter_location_not_found", **{"location": location}
                )

            # call API with location as entity parameter e.g. KBAbstractionLayer("lockdown", "amahoro")
            # if response == "yes":
            #   isOrIsNot = "is"
            # else:
            #   response = "No"
            #   isOrIsNot = "is not"

            dispatcher.utter_message(
                text=f"{status}, {location} {isOrIsNot} under lockdown"
            )  # switch text -> response if response will be provided through domain.yml e.g utter_xxx_xxx

            # dispatcher.utter_message(
            #     text=f"{location} is under lockdown"
            # )  # switch text -> response if response will be provided through domain.yml e.g utter_xxx_xxx

        else:
            dispatcher.utter_message(response="utter_ask_location")

        return []
