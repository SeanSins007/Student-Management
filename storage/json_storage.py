# storage/json_storage.py

import json
import os
from typing import Any, List, Type
from utils.msg import (
    error, 
    success, 
    info, 
    warning, 
    # heading, 
    # subheading
)


class JSONStorage:
    """A simple JSON file-based storage for objects with to_dict/from_dict methods."""

    def __init__(self, filename: str):
        self.filename = filename
        folder = os.path.dirname(filename)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)
            info(f"Created folder for storage: {folder}")
        if not os.path.exists(filename):
            self.save([])
            info(f"Initialized storage file: {filename}")
        else:
            info(f"Storage file loaded: {filename}")

    def load(self, cls: Type) -> List[Any]:
        """Load data from JSON file and return a list of class instances."""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data_list = json.load(f)
            instances = [cls.from_dict(item) for item in data_list]
            info(f"Loaded {len(instances)} items from {self.filename}")
            return instances
        except (json.JSONDecodeError, FileNotFoundError):
            warning(f"Failed to load {self.filename}. Returning empty list.")
            return []

    def save(self, items: List[Any]):
        """Save a list of objects to JSON."""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([item.to_dict() for item in items], f, indent=4)
        success(f"Saved {len(items)} items to {self.filename}")

    def add(self, item: Any):
        """Add a single item to storage."""
        items = self.load(item.__class__)
        items.append(item)
        self.save(items)
        success(f"Added new item: {getattr(item, 'name', getattr(item, 'student_id', getattr(item, 'teacher_id', 'Unknown')))}")

    def update(self, updated_item: Any, key: str = "id"):
        """Update an existing item based on a unique key."""
        items = self.load(updated_item.__class__)
        for idx, item in enumerate(items):
            if getattr(item, key, None) == getattr(updated_item, key, None):
                items[idx] = updated_item
                self.save(items)
                success(f"Updated item with {key}={getattr(updated_item, key)}")
                return
        error(f"Update failed: no item with {key}={getattr(updated_item, key)} found.")

    def delete(self, item_id: str, cls: Type, key: str = "id"):
        """Delete an item by key."""
        items = self.load(cls)
        new_items = [item for item in items if getattr(item, key, None) != item_id]
        if len(new_items) == len(items):
            error(f"Delete failed: no item with {key}={item_id} found.")
        else:
            self.save(new_items)
            success(f"Deleted item with {key}={item_id}")
