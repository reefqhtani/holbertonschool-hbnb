class InMemoryRepository:
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj
        return obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if not obj:
            return None
        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        return obj

    def delete(self, obj_id):
        return self._storage.pop(obj_id, None)

import uuid


class Repository:
    """In-memory repository"""

    def __init__(self):
        self._data = {
            "User": {},
            "Place": {},
            "Review": {},
            "Amenity": {}
        }

    def add(self, obj_type, obj):
        """Add object to repository"""
        self._data[obj_type][obj.id] = obj

    def get(self, obj_type, obj_id):
        """Get object by ID"""
        return self._data[obj_type].get(obj_id)

    def all(self, obj_type):
        """Get all objects of a type"""
        return list(self._data[obj_type].values())

    def delete(self, obj_type, obj_id):
        """Delete object by ID"""
        if obj_id in self._data[obj_type]:
            del self._data[obj_type][obj_id]
