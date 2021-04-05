def convert_item_tuples(tuples):
    result = []

    for t in tuples:
        result.append({'id': t[0], 'name': t[1]})

    return result


def convert_csv_to_list(value):
    return [(item.strip(),) for item in value.split(',')]
