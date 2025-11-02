# Country Capital Prediction - TCP Socket Application

A TCP socket-based client-server application for predicting country capitals.

## Overview

This project implements a country capital prediction game using TCP sockets in Python. The server reads country-capital pairs from an Excel file and challenges clients to guess the capital cities.

## Features

- **TCP Socket Communication**: Uses Python's socket library for reliable data transmission
- **Multi-Client Support**: Server handles multiple client connections sequentially
- **Input Validation**: Validates numeric inputs, country names, and capital cities
- **Attempt Management**: Provides 3 attempts for each capital city question
- **Graceful Termination**: Handles END commands and connection errors properly
- **Error Handling**: Comprehensive try/except blocks for network errors

## Project Structure

```
├── server.py              # Server implementation
├── client.py              # Client implementation
├── country_capital_list.xlsx  # Country-capital data file
└── README.md             # This file
```

## Requirements

- Python 3.x
- pandas (for reading Excel files)
- openpyxl (for Excel file support)

Install dependencies:
```bash
pip install pandas openpyxl
```

## How to Run

### 1. Start the Server

Open a terminal and run:
```bash
python server.py
```

The server will start listening on `127.0.0.1:65432`.

### 2. Start the Client

Open another terminal and run:
```bash
python client.py
```

The client will connect to the server and display the question.

## Usage

1. Server sends a question: "What is the capital city of [Country]?"
2. Client receives user input (capital city guess)
3. Server validates the input:
   - If correct: "Correct! [Capital] is the capital of [Country]."
   - If wrong: "Wrong answer. Attempts left: X. Try again:"
   - If numeric: "Numeric input is not allowed for capital names."
   - If country name: "'[Input]' is the name of a country, not a capital city."
4. Client has 3 attempts to guess correctly
5. Type "END" to terminate the session

## Error Handling

The application handles various network errors:
- **Connection Refused**: When server is not running
- **Sudden Disconnections**: During data transmission
- **File Not Found**: When Excel file is missing
- **Keyboard Interrupt**: Graceful shutdown with Ctrl+C

## Technical Details

### Server Side
- Reads country-capital pairs from Excel file
- Randomly selects a country for each client session
- Validates all client inputs
- Manages attempt limits
- Handles multiple client connections sequentially

### Client Side
- Establishes TCP connection to server
- Receives questions and displays them
- Sends user predictions
- Handles server responses appropriately
- Manages connection states

## License

This project is created for educational purposes as part of CMPE 472 - Computer Networks course.

