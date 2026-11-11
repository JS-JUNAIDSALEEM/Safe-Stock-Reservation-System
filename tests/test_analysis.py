import unittest
import json
import os
import tempfile


from main import (
    reserve_product,
    load_inventory,
    save_inventory,
    process_reservation,
    validate_inventory,
    InvalidQuantityError,
    InsufficientStockError,
    ProductNotFoundError
)


class TestSafeStockReservation(unittest.TestCase):

    def setUp(self):
        self.inventory = {"pen": 10, "book": 5}
        self.events = []


# Test 1: Successful reservation

    def test_successful_reservation(self):
        result = reserve_product(self.inventory, "pen", 4, self.events)

        self.assertEqual(result, 6)
        self.assertEqual(self.inventory["pen"], 6)
        self.assertEqual(self.events, ["reserved"])


# Test 2: Zero quantity

    def test_zero_quantity(self):
        with self.assertRaises(InvalidQuantityError):
            reserve_product(self.inventory, "pen", 0, self.events)

        self.assertEqual(self.inventory["pen"], 10)


# Test 3: Negative quantity

    def test_negative_quantity(self):
        with self.assertRaises(InvalidQuantityError):
            reserve_product(self.inventory, "pen", -2, self.events)

        self.assertEqual(self.inventory["pen"], 10)


# Test 4: Decimal quantity

    def test_decimal_quantity(self):
        with self.assertRaises(InvalidQuantityError):
            reserve_product(self.inventory, "pen", 2.5, self.events)

        self.assertEqual(self.inventory["pen"], 10)


# Test 5: Boolean quantity

    def test_boolean_quantity(self):
        with self.assertRaises(InvalidQuantityError):
            reserve_product(self.inventory, "pen", True, self.events)

        self.assertEqual(self.inventory["pen"], 10)


# Test 6: Insufficient stock

    def test_insufficient_stock(self):
        with self.assertRaises(InsufficientStockError):
            reserve_product(self.inventory, "pen", 15, self.events)

        self.assertEqual(self.inventory["pen"], 10)
        self.assertEqual(self.events, [])


# Test 7: Product not found

    def test_product_not_found(self):
        with self.assertRaises(ProductNotFoundError):
            reserve_product(self.inventory, "laptop", 2, self.events)

        self.assertEqual(self.inventory["pen"], 10)


# Test 8: Invalid inventory structure

    def test_invalid_inventory_structure(self):
        with self.assertRaises(ValueError):
            validate_inventory(["pen", 10])


# Test 9: Negative stock

    def test_negative_stock(self):
        with self.assertRaises(ValueError):
            validate_inventory({"pen": -5})


# Test 10: Invalid stock value

    def test_invalid_stock_value(self):
        with self.assertRaises(ValueError):
            validate_inventory({"pen": 5.5})


# Test 11: Invalid event list

    def test_invalid_events(self):
        with self.assertRaises(TypeError):
            reserve_product(self.inventory, "pen", 2, "invalid")

        self.assertEqual(self.inventory["pen"], 10)


# Test 12: Successful inventory loading

    def test_load_inventory_success(self):
        with tempfile.TemporaryDirectory() as folder:
            filename = os.path.join(folder, "inventory.json")

            with open(filename, "w", encoding="utf-8") as file:
                json.dump(self.inventory, file)

            result = load_inventory(filename)

            self.assertEqual(result, self.inventory)


# Test 13: Invalid JSON file

    def test_invalid_json(self):
        with tempfile.TemporaryDirectory() as folder:
            filename = os.path.join(folder, "inventory.json")

            with open(filename, "w", encoding="utf-8") as file:
                file.write("{invalid json}")

            with self.assertRaises(ValueError):
                load_inventory(filename)


# Test 14: Missing inventory file

    def test_missing_inventory_file(self):
        with tempfile.TemporaryDirectory() as folder:
            filename = os.path.join(folder, "missing.json")

            with self.assertRaises(FileNotFoundError):
                load_inventory(filename)


# Test 15: Successful file-based reservation

    def test_process_reservation_success(self):
        with tempfile.TemporaryDirectory() as folder:
            filename = os.path.join(folder, "inventory.json")

            with open(filename, "w", encoding="utf-8") as file:
                json.dump(self.inventory, file)

            result = process_reservation(filename, "pen", 4, self.events)
            saved_inventory = load_inventory(filename)

            self.assertEqual(result, 6)
            self.assertEqual(saved_inventory["pen"], 6)
            self.assertEqual(self.events, ["reserved"])


# Test 16: Failed reservation preserves original data

    def test_process_reservation_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            filename = os.path.join(folder, "inventory.json")

            original_inventory = self.inventory.copy()
            self.events = ["previous_event"]

            with open(filename, "w", encoding="utf-8") as file:
                json.dump(original_inventory, file)

            with self.assertRaises(InsufficientStockError):
                process_reservation(filename, "pen", 20, self.events)

            self.assertEqual(load_inventory(filename), original_inventory)
            self.assertEqual(self.events, ["previous_event"])


# Test 17: Serialization failure preserves original JSON

    def test_save_inventory_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            filename = os.path.join(folder, "inventory.json")

            original_inventory = {"pen": 10}

            with open(filename, "w", encoding="utf-8") as file:
                json.dump(original_inventory, file)

            invalid_inventory = {"pen": 10, "invalid": {1, 2, 3}}

            with self.assertRaises(TypeError):
                save_inventory(invalid_inventory, filename)

            self.assertEqual(load_inventory(filename), original_inventory)

            temp_files = [
                file for file in os.listdir(folder)
                if file.endswith(".temp")
            ]

            self.assertEqual(temp_files, [])


if __name__ == "__main__":
    unittest.main()