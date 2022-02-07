from config.AlertProperties import AlertPriority
from data.AlertExamples import alerts
import SerachPatternAlgorithm

import ciso8601
import time
import operator

configCherryPickNum = 4
topPriorityAlerts = []
priorityLevelsMatchingAlerts = [dict() for num in range(len(AlertPriority.templates))]
newPriorityConfig = {}


def get_alert_id(alert):
    return alert['_id']


def get_alert_type_key(alert):
    return alert['Details']['Type'] + "_" + alert['Details']['SubType']


def get_alert_timestamp(alert):
    """
    This function converts the timestamp into unix time in order to properly sort by most recent alerts
    ciso8601 seems to be the fastest way.
    :param alert:
    :return:
    """
    parsed_time = ciso8601.parse_datetime(alert.get('FoundDate'))
    return time.mktime(parsed_time.timetuple()) + parsed_time.microsecond / 1e6


def types_match(in_alert, rule):
    # Comparing type and subtype
    if rule['alert_type'] == in_alert['Details']['Type'] \
            and rule['alert_subtype'] == in_alert['Details']['SubType']:
        return True

    return False


def find_match(in_alert):
    # Iterating the alert over priority map,
    # Calling for types match if the titles matched. then and return a priority # on full match
    type_key_match = newPriorityConfig.get(get_alert_type_key(in_alert))
    if not type_key_match:
        return -1

    for title in type_key_match.items():
        if SerachPatternAlgorithm.KMPSearch(title[0], in_alert['Title']):
            return title[1]  # priority number

    return -1


def find_full_matches(incoming_alerts):
    """
    This function iterate over incoming alerts and match it against the priority config
    1. An iteration is done each alert over the priority level config from top priority to lowest
    2. First an attempt is made to find a matching type subtype
    3. If found then a comparison of titles is made (if not found it continue with same alert to the next priority rule)
    4. If a full match is found it insert the alert ID and timestamp into the matching alerts map.
    :param incoming_alerts:
    :return:
    """
    for in_alert in incoming_alerts:
        priority_lvl_match = find_match(in_alert)
        if priority_lvl_match != -1:
            priorityLevelsMatchingAlerts[priority_lvl_match].update(
                {get_alert_id(in_alert): float(get_alert_timestamp(in_alert))})


def order_matches_by_most_recent():
    """
    Sorting the matching alerts per priority by most recent according to timestamp.
    This seems to be the fastest way.
    TODO - search for faster way - tuple sort? quickSort? sorted insertion?
    :return:
    """
    for idx, priorityMatches in enumerate(priorityLevelsMatchingAlerts):
        priorityLevelsMatchingAlerts[idx] = \
            {k: v for k, v in sorted(priorityMatches.items(), key=operator.itemgetter(1), reverse=True)}


def cherry_pick_top_alerts():
    """
    This function iterate over the list of matching alerts by priority,
    From the top priority, down to the lowest one.
    For each priority a sorting to all the matching alerts by most recent timestamp is done
    The end results will be the topPriorityAlerts list filled with the (configured) cherry-picked top priority alerts
    :return:
    """
    cherry_pick_iter = 0
    print("Top priority alert IDs are:")
    for priorityAlerts in priorityLevelsMatchingAlerts:
        for priorityAlert in priorityAlerts.items():
            if cherry_pick_iter < configCherryPickNum:
                topPriorityAlerts.append(priorityAlert[0])
                print("Alert ID:", priorityAlert[0])
                cherry_pick_iter += 1
    print("Total top priority alerts found:", "[", cherry_pick_iter, "] out of", "[", configCherryPickNum, "]")


def find_top_priority_alerts(incoming_alerts):
    """
    Implement logic algorithm is as follows:
    1. first it takes the alerts priority rule map and prepare a new priority rule map called 'newPriorityConfig'
        1.1. the newPriorityConfig is a dictionary where:
            the key is: 'type_subtype'
            the value is: a dictionary where
                the key is: title
                the value is: priority number
            meaning it inserts all the titles and thier priority number,
            that are connected to this type and subtype as key:value pairs
    2. find_full_matches()
        2.1. first it finds a type_subtype key within the newPriorityConfig dictionary
        2.2. then try to match any of its titles to the alert title (if found, the priority number is returned as value)
        2.3. each match will be inserted into the list.
        2.4. each element in the list represents a priority level and contains a dictionary,
        Of all the matched alerts with the same priority level.
        2.5. The dictionary key will be the alert ID since it is unique (AFAIK)
        and the value will be the alert timestamp
    4. order_matches_by_most_recent() sort the dictionary of each 'priority level list element' by timestamp
    in order to pick the most recent
    5. cherry_pick_top_alerts() - iterate over the priority level list from the highest priority (1) and cherry-pick
    a configured amount of alerts, first by priority level then sorted by time.

    :param incoming_alerts:
    :return:
    """
    find_full_matches(incoming_alerts)
    order_matches_by_most_recent()
    cherry_pick_top_alerts()


def load_priority_rule_map():
    """
    takes the alerts priority rule map and prepare a new priority rule map called 'newPriorityConfig'
    the newPriorityConfig is a dictionary where:
    the key is: 'type_subtype'
    the value is: a dictionary where
        the key is: title
        the value is: priority number
    meaning it inserts all the titles and thier priority number,
    that are connected to this type and subtype as key:value pairs
    :return:
    """
    config = AlertPriority.templates
    for priorityValue in config.items():
        for option in priorityValue[1]:
            key = option.get('alert_type') + '_' + option.get('alert_subtype')
            for title in option.get('title_identifiers'):
                key_found = newPriorityConfig.get(key)
                if key_found:
                    key_found.update({title: priorityValue[0]})
                else:
                    newPriorityConfig.update({key: {title: priorityValue[0]}})


if __name__ == '__main__':
    load_priority_rule_map()
    find_top_priority_alerts(alerts)
