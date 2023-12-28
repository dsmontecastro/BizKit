import time
from flask import Blueprint

from .data.match_data import MATCHES


bp = Blueprint("match", __name__, url_prefix="/match")


@bp.route("<int:match_id>")
def match(match_id):
    if match_id < 0 or match_id >= len(MATCHES):
        return "Invalid match id", 404

    start = time.time()
    msg = "Match found" if (is_match(*MATCHES[match_id])) else "No match"
    end = time.time()

    return {"message": msg, "elapsedTime": end - start}, 200




def is_match(fave_numbers_1: list[int], fave_numbers_2: list[int]):
    """
    Match two lists of integers (equality).

    Comparison
    ----------
        MATCHES[2]: From ~40+s to ~1s.
        MATCHES[3]: From ~45+s to <1s.

    Parameters
    ----------
        fave_numbers_1 : list[int]
            numbers to match against
        fave_numbers_2 : list[int]
            numbers to compare

    Returns
    -------
    boolean
        whether or not all integers in fave_numbers_2 are in fave_numbers_1
    """
    
    # [ADD] 'Clean' lists for easier processing.
    faves_1 = clean(fave_numbers_1)
    faves_2 = clean(fave_numbers_2)


    for num in faves_2:

        # [ADD] Remove matched elements from <faves_2>,
        # ----- to remove redundant comparisons.

        try:
            ind = faves_1.index(num)
            faves_1.pop(ind)

        except ValueError: return False

    return True



def clean(nums: list[int]):
    """
    'Cleans up' a list of integers.

    Parameters
    ----------
    nums: list[int]
        list to be 'cleaned'

    Returns
    -------
        a sorted list of integers without duplicate elements
    """

    return sorted(set(nums))