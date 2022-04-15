class Inventory(dict):
    def to_json(self) -> 'dict':
        return {item.name: amount for item, amount in self.items()}

    @staticmethod
    def from_json(json_object: 'dict') -> 'Inventory':
        from world.items import Items

        if json_object:
            return {Items.get_item_by_name(item): amount for item, amount in json_object.items()}
        return dict()
