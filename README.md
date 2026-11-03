
# Library Management System

A beginner-friendly Library Management System built with **Python** and **Streamlit** to manage books, members, and borrow/return records.

## Features

- Add and view books in the library
- Register and manage members
- Borrow and return books
- Track borrow/return records
- Data saved in `library.json`

## Tech Stack

- Python 3
- Streamlit
- JSON (for data storage)

## Project Structure

```
library-management-system/
├── main.py          # Streamlit app
├── library.json     # Stored library data
├── requirements.txt # Dependencies
└── README.md
```

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/rohitttdurangiii/library-management-system.git
   cd library-management-system
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the app:
   ```bash
   streamlit run main.py
   ```
4. Open the link shown in the terminal (usually http://localhost:8501).

## What I Learned

- Building a web interface with Streamlit
- Reading and writing data with JSON files
- Structuring a small Python project

## Future Improvements

- Search and filter books
- Due dates and fine calculation
- Move storage from JSON to SQLite
- Login for librarian and members

## Author

Rohit Tirmale
