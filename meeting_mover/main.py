from data import test_cases
from typing import List, Tuple
from collections import defaultdict


def conflict(meeting_map, i, j):
    """
    Checks whether meeting i and j share attendee.
    """
    for attendee in meeting_map[i]:
        if attendee in meeting_map[j]:
            return True
    return False


def find_meeting_subsets(meetings: List[List[int]]) -> Tuple[List[List[int]], int]:
    """
    This problem can be interpreted as a maximum weighted independent set problem,
    where each node in the graph would be the meeting and each edge represents conflicting attendence.
    Weight of each node is the number of participants in the meeting, aka size of meeting array.
    Maximum weighted independent set problem is known to be NP-hard and can only be solved in
    exponential time precisely. Hence we use a greedy algorithm here and return an approximated result.

    1. Choose an available meeting with maximum number of attendee
    2. Add the meeting to the result set
    3. Remove its adjacent meeting from the available meeting set
    4. If there are still available meetings, go to step 1.
        Otherwise return the result set and total number of attendee.
    """
    meeting_map = {}
    conflicting_graph = defaultdict(set)
    n = len(meetings)

    for i in range(n - 1):
        for j in range(i + 1, n):
            if i not in meeting_map:
                meeting_map[i] = set(meetings[i])
            if j not in meeting_map:
                meeting_map[j] = set(meetings[j])
            if conflict(meeting_map, i, j):
                conflicting_graph[i].add(j)
                conflicting_graph[j].add(i)

    available_meetings = set()

    for i in range(n):
        available_meetings.add(i)

    result_set = []
    total_number_of_attendee = 0

    while available_meetings:
        meeting_to_choose = None
        number_of_attendee = -float("inf")

        for i in available_meetings:
            if len(meetings[i]) > number_of_attendee:
                number_of_attendee = len(meetings[i])
                meeting_to_choose = i

        available_meetings.remove(meeting_to_choose)
        result_set.append(meetings[meeting_to_choose])
        total_number_of_attendee += number_of_attendee

        for j in conflicting_graph[meeting_to_choose]:
            if j in available_meetings:
                available_meetings.remove(j)

    return result_set, total_number_of_attendee


if __name__ == "__main__":
    for i, test_case in enumerate(test_cases):
        print("==========================")
        print(f"Test {i}:")
        result_set, total_number_of_attendee = find_meeting_subsets(test_case)
        print(f"Result Set: {result_set}")
        print(f"Total number of attendee: {total_number_of_attendee}")
