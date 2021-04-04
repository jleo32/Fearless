class Item(object):
    """
    Holder for item information to and from database

    item_id used because `id` is used by Python
    """
    def __init__(self, item_id, name):
        self.item_id = item_id
        self.name = name
