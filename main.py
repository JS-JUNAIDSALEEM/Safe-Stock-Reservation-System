# Project: Safe Stock Reservation System
# This project reserves product stock safely and saves changes in a JSON file.

import json
import os
import tempfile

# CUSTOM EXCEPTIONS

class InventoryError(Exception):
    pass


class InvalidQuantityError(InventoryError):
    pass


class InsufficientStockError(InventoryError):
    pass


class ProductNotFoundError(InventoryError):
    pass


# VALIDATE INVENTORY

def validate_inventory(data):

    if not isinstance(data, dict):
        raise ValueError("Inventory data must be a JSON object.")

    for name, stock in data.items():

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product names must be non-empty strings.")

        if isinstance(stock, bool) or not isinstance(stock, int) or stock < 0:
            raise ValueError(f"Stock for '{name}' must be a non-negative whole number.")

    return data


# RESERVE PRODUCT

def reserve_product(inventory, name, quantity, events):

    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
        raise InvalidQuantityError("Quantity must be a positive whole number.")

    if not isinstance(events, list):
        raise TypeError("Events must be a list.")

    validate_inventory(inventory)

    if not isinstance(name, str) or not name.strip():
        raise ProductNotFoundError("Product name must be a non-empty string.")

    if name not in inventory:
        raise ProductNotFoundError(f"Product '{name}' not found in inventory.")

    stock = inventory[name]

    if quantity > stock:
        raise InsufficientStockError("Insufficient stock")

    remaining = stock - quantity

    inventory[name] = remaining
    events.append("reserved")

    return remaining


# LOAD INVENTORY FROM JSON FILE

def load_inventory(filename):

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        return validate_inventory(data)

    except FileNotFoundError:
        raise FileNotFoundError("Inventory file not found.")

    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON format in '{filename}': {error}")


# SAVE INVENTORY SAFELY

def save_inventory(data, filename):

    temp_filename = None

    try:
        # Validate data before creating or replacing the inventory file.
        validate_inventory(data)

        directory = os.path.dirname(os.path.abspath(filename))

        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=directory,
            prefix="inventory_",
            suffix=".temp",
            delete=False
        ) as file:

            temp_filename = file.name

            try:
                json.dump(data, file, indent=4)
            except TypeError as error:
                raise TypeError(
                    f"Serialization failed. Data contains non-serializable objects: {error}"
                )

        os.replace(temp_filename, filename)

    finally:
        if temp_filename and os.path.exists(temp_filename):
            try:
                os.remove(temp_filename)
            except OSError:
                pass


# PROCESS RESERVATION

def process_reservation(filename, name, quantity, events):

    if not isinstance(events, list):
        raise TypeError("Events must be a list.")

    events_backup = list(events)

    try:
        inventory = load_inventory(filename)

        updated_stock = reserve_product(inventory, name, quantity, events)
        save_inventory(inventory, filename)
        return updated_stock

    except Exception:
        events[:] = events_backup
        raise


# TEST 1: Successful reservation

def test_successful_reservation():
    inventory = {"pen": 10}
    events = []
    result = reserve_product(inventory, "pen", 4, events)

    assert result == 6
    assert inventory == {"pen": 6}
    assert events == ["reserved"]


# TEST 2: Invalid quantity

def test_reserve_product_invalid_quantity():
    inventory = {"pen": 10}
    events = []
    inv = inventory.copy()
    eve = events.copy()

    try:
        reserve_product(inventory, "pen", 0, events)
        assert False, "Expected InvalidQuantityError."

    except InvalidQuantityError as error:
        assert str(error) == "Quantity must be a positive whole number."

    assert inventory == inv
    assert events == eve


# TEST 3: Insufficient stock

def test_reserve_product_insufficient_stock():
    inventory = {"pen": 10}
    events = []
    inv = inventory.copy()
    eve = events.copy()

    try:
        reserve_product(inventory, "pen", 15, events)
        assert False, "Expected InsufficientStockError."

    except InsufficientStockError as error:
        assert str(error) == "Insufficient stock"

    assert inventory == inv
    assert events == eve


# TEST 4: Product not found

def test_product_not_found():
    inventory = {"pen": 10}
    events = []

    try:
        reserve_product(inventory, "book", 2, events)
        assert False, "Expected ProductNotFoundError."

    except ProductNotFoundError:
        pass

    assert inventory == {"pen": 10}
    assert events == []


# TEST 5: Successful file-based reservation

def test_process_reservation_success():

    with tempfile.TemporaryDirectory() as folder:
        filename = os.path.join(folder, "inventory.json")

        with open(filename, "w", encoding="utf-8") as file:
            json.dump({"pen": 10}, file)

        events = []

        result = process_reservation(filename, "pen", 4, events)
        saved_inventory = load_inventory(filename)

        assert result == 6
        assert saved_inventory == {"pen": 6}
        assert events == ["reserved"]


# TEST 6: Validation failure preserves file and events

def test_process_reservation_failure():

    with tempfile.TemporaryDirectory() as folder:
        filename = os.path.join(folder, "inventory.json")

        original_data = {"pen": 10}
        events = ["previous_event"]

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(original_data, file)

        try:
            process_reservation(filename, "pen", 15, events)
            assert False, "Expected InsufficientStockError"

        except InsufficientStockError:
            pass

        assert load_inventory(filename) == original_data
        assert events == ["previous_event"]


# TEST 7: Invalid quantity in file-based reservation

def test_process_reservation_invalid_quantity():

    with tempfile.TemporaryDirectory() as folder:
        filename = os.path.join(folder, "inventory.json")

        original_data = {"pen": 10}
        events = ["previous_event"]
        original_events = events.copy()

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(original_data, file)

        try:
            process_reservation(filename, "pen", 0, events)
            assert False, "Expected InvalidQuantityError"

        except InvalidQuantityError as error:
            assert str(error) == "Quantity must be a positive whole number."

        assert load_inventory(filename) == original_data
        assert events == original_events


# TEST 8: Invalid inventory data is not saved

def test_save_inventory_invalid_data():

    with tempfile.TemporaryDirectory() as folder:
        filename = os.path.join(folder, "inventory.json")
        original_data = {"pen": 10}

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(original_data, file)

        invalid_data = {"pen": -5}

        try:
            save_inventory(invalid_data, filename)
            assert False, "Expected ValueError"

        except ValueError:
            pass

        assert load_inventory(filename) == original_data

        temp_files = [
            file for file in os.listdir(folder)
            if file.endswith(".temp")
        ]
        assert temp_files == []


# TEST 9: Invalid JSON file

def test_load_invalid_json():

    with tempfile.TemporaryDirectory() as folder:
        filename = os.path.join(folder, "inventory.json")

        with open(filename, "w", encoding="utf-8") as file:
            file.write("{invalid json}")

        try:
            load_inventory(filename)
            assert False, "Expected ValueError."

        except ValueError as error:
            assert "Invalid JSON format" in str(error)


# TEST 10: Missing inventory file

def test_load_missing_file():

    with tempfile.TemporaryDirectory() as folder:
        filename = os.path.join(folder, "missing.json")

        try:
            load_inventory(filename)
            assert False, "Expected FileNotFoundError."

        except FileNotFoundError as error:
            assert str(error) == "Inventory file not found."


# OUTPUT SECTION: Run All Tests

def main():

    tests = [
        test_successful_reservation,
        test_reserve_product_invalid_quantity,
        test_reserve_product_insufficient_stock,
        test_product_not_found,
        test_process_reservation_success,
        test_process_reservation_failure,
        test_process_reservation_invalid_quantity,
        test_save_inventory_invalid_data,
        test_load_invalid_json,
        test_load_missing_file,
    ]

    print("\n===== SAFE STOCK RESERVATION SYSTEM TESTS =====\n")

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("\n===== ALL 10 TESTS PASSED =====")


if __name__ == "__main__":
    main()