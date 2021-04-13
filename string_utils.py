import re

def get_first_string_between_substrings(base_string, start_string, end_string):
    try:
        after_start_string = s.split(start_string)[1]
        before_end_string_and_after_start_string = after_start_string.split(end_string)[0]
        return before_end_string_and_after_start_string
    except IndexError:
        return None

def pad_int(num, desired_length):
    num_str = str(num)
    num_str_len = len(num_str)
    assert num_str_len <= desired_length
    return '0' * (num_str_len - desired_length) + num_str