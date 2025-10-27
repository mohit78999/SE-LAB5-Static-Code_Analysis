"""
Inventory Management System

A simple inventory management system that allows adding, removing,
and tracking items in stock. Supports persistent storage using JSON.
"""

import json
from datetime import datetime

# Global variable for inventory state
stock_data = {}


def add_item(item="default", qty=0, logs=None):
    """
    Add quantity of an item to inventory.

    Args:
        item: Item identifier (string/int)
        qty: Quantity to add (int)
        logs: Optional list to track operations

    Returns:
        None
    """
    if logs is None:
        logs = []
    if not item:
        return
    try:
        qty = int(qty)
        stock_data[item] = stock_data.get(item, 0) + qty
        logs.append(f"{datetime.now()}: Added {qty} of {item}")
    except ValueError:
        return  # Invalid quantity provided


def remove_item(item, qty):
    """
    Remove quantity of an item from inventory.

    Args:
        item: Item identifier (string/int)
        qty: Quantity to remove (int)

    Returns:
        None
    """
    try:
        qty = int(qty)
        if item in stock_data:
            stock_data[item] -= qty
            if stock_data[item] <= 0:
                del stock_data[item]
    except (KeyError, ValueError) as error:
        print(f"Error removing item: {error}")


def get_qty(item):
    """
    Get current quantity of an item.

    Args:
        item: Item identifier (string/int)

    Returns:
        int: Current quantity in stock (0 if not found)
    """
    return stock_data.get(item, 0)


def load_data(filepath="inventory.json"):
    """
    Load inventory data from JSON file.

    Args:
        filepath: Path to JSON file (default: inventory.json)

    Returns:
        None
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            global stock_data
            stock_data = json.load(file)
    except FileNotFoundError:
        print(f"Warning: {filepath} not found. Starting with empty inventory.")
    except json.JSONDecodeError:
        print(f"Warning: {filepath} contains invalid JSON. Starting fresh.")


def save_data(filepath="inventory.json"):
    """
    Save inventory data to JSON file.

    Args:
        filepath: Path to JSON file (default: inventory.json)

    Returns:
        None
    """
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(stock_data, file, indent=2)


def print_data():
    """
    Print current inventory report to console.

    Returns:
        None
    """
    print("Items Report")
    for item_name, quantity in stock_data.items():
        print(f"{item_name} -> {quantity}")


def check_low_items(threshold=5):
    """
    Check for items with stock below threshold.

    Args:
        threshold: Minimum quantity threshold (default: 5)

    Returns:
        list: Items with quantity below threshold
    """
    return [item for item, qty in stock_data.items() if qty < threshold]


def main():
    """Execute main program sequence."""
    add_item("apple", 10)
    add_item("banana", -2)
    add_item(123, "ten")  # Invalid quantity - will be ignored
    remove_item("apple", 3)
    remove_item("orange", 1)
    print("Apple stock:", get_qty("apple"))
    print("Low items:", check_low_items())
    save_data()
    load_data()
    print_data()


if __name__ == "__main__":
    main()

