from config.AlertProperties import AlertPriority
from data.AlertExamples import alerts

import ciso8601
import time
import operator
import SerachPatternAlgorithm

configCherryPickNum = 4
topPriorityAlerts = []
priorityLevelsMatchingAlerts = [dict() for num in range(len(AlertPriority.templates))]


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


def types_match(in_alert, rule):
    # Comparing type and subtype
    if rule['alert_type'] == in_alert['Details']['Type'] \
            and rule['alert_subtype'] == in_alert['Details']['SubType']:
        return True

    return False


def find_match(in_alert):
    # Iterating the alert over priority map,
    # And if titles match we send for types match and return a priority # on full match
    for priority in AlertPriority.templates.items():
        for rule in priority[1]:
            for title in rule['title_identifiers']:
                if SerachPatternAlgorithm.KMPSearch(title, in_alert['Title']) \
                        and types_match(in_alert, rule):
                    return priority[0]
    return -1


def find_full_matches(incoming_alerts):
    """
    This function iterate over incoming alerts and match it against the priority config
    1. We iterate each alert over the priority level config from top priority to lowest
    2. First we try to find a matching title
    3. If found then we compare subtype and type (if not found we continue with same alert to the next priority rule)
    4. If a full match is found we insert the alert ID and timestamp into the matching alerts map.
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
    For each priority we sort all the matching alerts by most recent timestamp
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
    Implement logic is as follows:
    1. We receive the incoming alerts file along with priority configuration mapping
    2. find_full_matches()
        2.1. first matches titles or contained titles
        2.2. then matches type and subtype
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


if __name__ == '__main__':
    find_top_priority_alerts(alerts)
