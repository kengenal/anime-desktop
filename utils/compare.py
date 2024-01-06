from typing import Dict, Set

from const.mal import Status


def compare_and_get_keys(d1: Dict, d2: Dict) -> Set[Status]:
    is_changed_in = set()
    for key, val in d1.items():
        if d2.get(key) != val:
            is_changed_in.add(key)
    return is_changed_in
