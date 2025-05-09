import re


def valid_time_format(time_str: str) -> bool:
    """
    Validate that a time string matches HH:MM:SS format.

    Args:
        time_str (str): The input string in HH:MM:SS format.

    Returns:
        (bool): True if match, False otherwise.
    """
    time_pattern = re.compile(r'^([0-1][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$')
    if not time_pattern.match(time_str):
        return False

    return True
