def convert_list_in_string(lst: list[dict[str, str]]) -> str:
    result = ''
    for item in lst:
        result += item['name'] + ', '
    return result[:-2]
