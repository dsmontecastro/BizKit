from flask import Blueprint, request

from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200



# Additional imports
from enum import IntEnum
from typing import Any


def search_users(args: dict[str, Any]):
    """
    Search users database

    Parameters
    ----------
        args: dict[str, Any]
            a dictionary containing the following search parameters:
                id:         string
                name:       string
                age:        string
                occupation: string

    Returns
    -------
    list[dict[str, Any]]
        a list of users that match the search parameters
    """


    ids: set[str] = set()               # Track User.IDs used to avoid duplicate entries.
    results: list[dict[str, Any]] = []  # Collect Users filtered using the <arg> parameters.


    # Iterate over <arg> parameters, using the order provided in the 'Bonus Challenge' section.
    for param in PARAMS:

        try:

            key = param.name.lower()
            value = args[key]


            filtered: list[dict[str, Any]] = []     # Filter <USERS> depending on the
            match(param):                           # specification(s) for each parameter.

                case PARAMS.ID:

                    def filter_eq(user: dict[str, Any]):
                        unique: bool = user["id"] not in ids
                        equal: bool = value == user[key]
                        return unique and equal

                    filtered += filter(filter_eq, USERS)


                case PARAMS.NAME | PARAMS.OCCUPATION:

                    def filter_in(user: dict[str, Any]):
                        unique: bool = user["id"] not in ids
                        inside: bool = value.lower() in user[key].lower()
                        return unique and inside

                    filtered += filter(filter_in, USERS)


                case PARAMS.AGE:

                    match = int(value)

                    def filter_range(user: dict[str, Any]):
                        unique: bool = user["id"] not in ids
                        in_range: bool = (match - 1) <= user[key] <= (match + 1)
                        return unique and in_range

                    filtered += filter(filter_range, USERS)


            for item in filtered: ids.add(item["id"])
            results += filtered


        # Skip parameters not found in <args>.
        except KeyError: pass


    return results



class PARAMS(IntEnum):
    """
    Enumeration Class for the given parameters.
    Uses 'IntNum' to preserve the order of items.
    Order is based on specification in the 'Bonus Challenge' section.
    """

    ID = 0
    NAME = 1
    AGE = 2
    OCCUPATION = 3