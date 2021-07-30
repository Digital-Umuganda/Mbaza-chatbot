from tests.conftest import EMPTY_TRACKER
from actions import actions


def test_action_check_statistics_successful(dispatcher, domain):
    tracker = EMPTY_TRACKER
    action = actions.ActionCheckStatistics()
    events = action.run(dispatcher, tracker, domain)
    expected_location = "Rwanda"
    expected_responses = ["utter_statistics", "utter_did_that_help"]
    expected_events = []

    assert dispatcher.messages[0]["location"] == expected_location
    for i, expected_response in enumerate(expected_responses):
        assert dispatcher.messages[i]["response"] == expected_response
    assert events == expected_events
