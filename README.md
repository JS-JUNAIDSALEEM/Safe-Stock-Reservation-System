# Safe Stock Reservation System

## Project Overview

The Safe Stock Reservation System is a Python project that manages product stock reservations safely. It checks product availability, validates reservation quantities, and updates inventory data stored in a JSON file.

The main purpose of this project is to make sure that stock is updated correctly and original inventory data is not damaged if an error occurs during a reservation.

## Features

- Reserve products from available stock.
- Check product availability before reservation.
- Validate reservation quantities.
- Handle insufficient stock and missing products.
- Use custom exceptions for different errors.
- Validate inventory data before using it.
- Load and save inventory data using JSON.
- Save inventory safely using a temporary file.
- Restore event records if a reservation fails.
- Run automated tests to check different success and failure cases.

## Technologies Used

- Python
- JSON
- File Handling
- Exception Handling
- Temporary Files
- Unittest for Automated Testing

## Project Structure

```text
Safe-Stock-Reservation-System/
│
├── tests/
│   └── test_analysis.py
│
├── Output/
│   └── Reservation Tests.png
│
├── main.py
├── README.md
├── requirements.txt
└── .gitignore
```

## How to Run

**Step 1:** Clone the repository.

```bash
git clone https://github.com/JS-JUNAIDSALEEM/Safe-Stock-Reservation-System.git
```

**Step 2:** Open the project folder.

```bash
cd Safe-Stock-Reservation-System
```

**Step 3:** Run the Python file.

```bash
python main.py
```

## Testing

The project includes 17 automated tests to check different parts of the reservation system.

The tests cover:

1. Successful product reservation.
2. Zero reservation quantity.
3. Negative reservation quantity.
4. Decimal reservation quantity.
5. Boolean reservation quantity.
6. Insufficient stock.
7. Product not found.
8. Invalid inventory structure.
9. Negative stock value.
10. Invalid stock value.
11. Invalid event records.
12. Successful inventory loading.
13. Invalid JSON file.
14. Missing inventory file.
15. Successful file-based reservation.
16. Reservation failure without changing original data.
17. Serialization failure without damaging the original file.

To run the automated tests, use:

```bash
py -m unittest tests/test_analysis.py -v 
```

Each test checks whether the system behaves correctly in different situations.

## What I Learned

While working on this project, I practiced:

- Creating and using custom exceptions.
- Working with JSON files in Python.
- Handling file errors.
- Validating inventory data.
- Using temporary files for safer data updates.
- Managing errors during a reservation process.
- Writing automated tests using unittest.
- Checking that original data remains unchanged when an operation fails.

## Future Improvements

- Add a product management system.
- Add reservation history.
- Connect the system with a database.
- Add support for multiple users.
- Build a simple user interface.

## Author

### Junaid Saleem

- **GitHub:** [JS-JUNAIDSALEEM](https://github.com/JS-JUNAIDSALEEM)
- **LinkedIn:** [Junaid Saleem](https://www.linkedin.com/in/junaid-saleem-developer/)