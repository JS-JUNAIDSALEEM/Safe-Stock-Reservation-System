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
- Load and save inventory data using JSON.
- Save inventory safely using a temporary file.
- Restore event records if a reservation fails.
- Run tests to check different success and failure cases.

## Technologies Used

- Python
- JSON
- File Handling
- Exception Handling
- Temporary Files
- Assertions for Testing

## Project Structure

```text
Safe-Stock-Reservation-System/
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

The project includes 10 tests to check different parts of the reservation system.

The tests cover:

1. Successful product reservation.
2. Invalid reservation quantity.
3. Insufficient stock.
4. Product not found.
5. Successful file-based reservation.
6. Reservation failure without changing original data.
7. Invalid quantity in file-based reservation.
8. Serialization failure.
9. Invalid JSON file.
10. Missing inventory file.

Each test checks whether the system behaves correctly in different situations.

## What I Learned

While working on this project, I practiced:

- Creating and using custom exceptions.
- Working with JSON files in Python.
- Handling file errors.
- Using temporary files for safer data updates.
- Managing errors during a reservation process.
- Writing tests using assertions.
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
