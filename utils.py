def convert_item_tuples(tuples):
    result = []

    for t in tuples:
        result.append({'id': t[0], 'name': t[1]})

    return result
