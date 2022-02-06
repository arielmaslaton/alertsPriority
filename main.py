from AlertProperties import AlertPriority
from AlertExamples import alerts

import ciso8601
import time
import operator

configCherryPickNum = 4
priorityConfig = {}
topPriorityAlerts = []
matchedAlertsByPriorityLvl = [dict() for num in range(len(AlertPriority.templates))]


def load_priority_config(config):
    """
    This function loads the alerts properties config,
    And creates a unique key for matching priority into incoming alerts.

    The key: shall consist of the following fields: <title_identifiers>_<alert_type>_<alert_subtype>
    The Value: shall be the priority of the specified rule

    If more then one title_identifiers are found, another key will be created, as we iterate all title_identifiers
    TODO - use strip() to improve performance
    :param config: alerts properties config
    :return:
    """
    for priorityValue in config.items():
        for option in priorityValue[1]:
            for title in option.get('title_identifiers'):
                priorityConfig.update(
                    {option.get('alert_type') + '_' + option.get('alert_subtype') + '_' + title: priorityValue[0]})


def get_key_from_alert(alert):
    return alert['Details']['Type'] + '_' + alert['Details']['SubType'] + '_' + alert['Title']


def get_alert_id(alert):
    return alert['_id']


def get_alert_timestamp(alert):
    """
    This function converts the timestamp into unix time in order to properly sort by most recent alerts
    ciso8601 seems to be the fastest way.
    :param alert:
    :return:
    """
    parsed_time = ciso8601.parse_datetime(alert.get('FoundDate'))
    return time.mktime(parsed_time.timetuple()) + parsed_time.microsecond / 1e6


def find_matches(incoming_alerts):
    """
    This function iterate over incoming alerts and match it against the priority config
    If a match is found we insert the alert into the matching alerts map.
    :param incoming_alerts:
    :return:
    """
    for alert in incoming_alerts:
        alert_key = get_key_from_alert(alert)
        # If the alert key was found then the priority number of the alert will be returned.
        # The returned priority number will be used to insert the alert ID and timestamp,
        # To the correct priority 'line' in matchingAlertsByPriority list.
        matching_alert_priority = priorityConfig.get(alert_key)
        if matching_alert_priority:
            matchedAlertsByPriorityLvl[matching_alert_priority] \
                .update({get_alert_id(alert): float(get_alert_timestamp(alert))})


def order_matches_by_most_recent():
    """
    Sorting the matching alerts per priority by most recent according to timestamp.
    This seems to be the fastest way.
    TODO - search for faster way - tuple sort? quickSort? insert into a sorted list
    :return:
    """
    for idx, priorityMatches in enumerate(matchedAlertsByPriorityLvl):
        matchedAlertsByPriorityLvl[idx] = \
            {k: v for k, v in sorted(priorityMatches.items(), key=operator.itemgetter(1), reverse=True)}


def cherry_pick_top_alerts():
    """
    This function iterate over the list of matching alerts by priority,
    From the top priority, down to the lowest one.
    For each priority we sort all the matching alerts by most recent timestamp
    The end results will be the topPriorityAlerts list filled with the (configured) cherry-picked top priority alerts
    :return:
    """
    cherry_pick_iter = 0
    print("Top priority alert IDs are:")
    for priorityAlerts in matchedAlertsByPriorityLvl:
        for priorityAlert in priorityAlerts.items():
            if cherry_pick_iter < configCherryPickNum:
                topPriorityAlerts.append(priorityAlert[0])
                print("Alert ID:", priorityAlert[0])
                cherry_pick_iter += 1
    print("Total top priority alerts found:", "[", cherry_pick_iter, "] out of", "[", configCherryPickNum, "]")


def find_top_priority_alerts(incoming_alerts):
    """
    Implement logic is as follows:
    1. main function loads the config alert properties into a key value dictionary, where the key is
    A unique string representing a unique match against an incoming alerts list
    2. find_matches() build a similar key from incoming alerts and find matches.
        2.1. each mach will be inserted into the list.
        2.2. each element in the list represents a priority level and contains a dictionary,
        Of all the matched alerts with the same priority level.
        2.3. The dictionary key will be the alert ID since it is unique (AFAIK)
        and the value will be the alert timestamp
    4. order_matches_by_most_recent() sort the dictionary of each 'priority level list element' by timestamp
    in order to pick the most recent
    5. cherry_pick_top_alerts() - iterate over the priority level list from the highest priority (1) and cherry-pick
    a configured amount of alerts, first by priority level then sorted by time.

    :param incoming_alerts:
    :return:
    """
    find_matches(incoming_alerts)
    order_matches_by_most_recent()
    cherry_pick_top_alerts()


if __name__ == '__main__':
    load_priority_config(AlertPriority.templates)
    find_top_priority_alerts(alerts)
