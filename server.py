#-----------------------------------------------------
# Title: Country Capital Prediction Server
# Author: Abdullah Esin
# ID: ************
# Section: 3
# Assignment: 1
# Description: This server implements a TCP socket-based country capital 
#              prediction application. It reads country-capital pairs from an Excel 
#              file, randomly selects a country, and allows clients to guess 
#              the capital city. The server handles multiple client connections, 
#              validates inputs, manages attempt limits, and gracefully handles 
#              client disconnections and END commands.
#-----------------------------------------------------

import socket
import pandas as pd
import random

# CONSTANTS AND CONFIGURATION
HOST = '127.0.0.1'  # Localhost - communication on the same computer
PORT = 65432        # Port number the server listens on
MAX_ATTEMPTS = 3    # Maximum number of guesses allowed for client
BUFFER_SIZE = 1024  # Buffer size for receiving data

# DATA LOADING - READING EXCEL FILE
def load_countries_data(filename='country_capital_list.xlsx'):

    try:
        # Read Excel file using pandas
        df = pd.read_excel(filename)
        
        # Take first two columns as country and capital
        # Create dictionary in {Country: Capital} format
        countries_dict = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))
        
        return countries_dict
    
    except FileNotFoundError:
        print(f"ERROR: File '{filename}' not found!")
        return {}
    except Exception as e:
        print(f"ERROR: Failed to read file: {e}")
        return {}

# CLIENT HANDLING - COMMUNICATION WITH A CLIENT
def handle_client(conn, addr, countries_dict):
    try:
        # Randomly select a country
        country = random.choice(list(countries_dict.keys()))
        correct_capital = countries_dict[country]
        # Send question to client
        question = f"What is the capital city of {country}? Your guess (or 'END' to finish):"
        conn.sendall(question.encode('utf-8'))
        # PREDICTION LOOP - Give client 3 guess attempts
        for attempt in range(1, MAX_ATTEMPTS + 1):

            # Receive prediction from client
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            
            prediction = data.decode('utf-8').strip()
            
            # "END" COMMAND CHECK
            if prediction.upper() == "END":
                response = "Session ended by client. Goodbye."
                conn.sendall(response.encode('utf-8'))
                conn.close()
                print("END received. Shutting down server.")
                return False
            
            # NUMERIC VALUE CHECK - Check if input is numeric value
            try:
                float(prediction)
                print("Numeric input is not allowed; closing connection.")
                response = "Numeric input is not allowed for capital names. Connection will close."
                conn.sendall(response.encode('utf-8'))
                break
            except ValueError:
                pass
            
            # CORRECT PREDICTION CHECK
            if prediction.lower() == correct_capital.lower():
                response = f"Correct! {correct_capital} is the capital of {country}. Closing connection."
                conn.sendall(response.encode('utf-8'))
                print("Correct; closing connection.")
                break
            
            # COUNTRY NAME CHECK
            is_country_name = False
            matched_country_name = None
            for ctry_name in countries_dict.keys():
                if prediction.lower() == ctry_name.lower():
                    is_country_name = True
                    matched_country_name = ctry_name
                    break
            
            if is_country_name:
                # Prediction is a country name, inform user and close connection
                response = f"'{prediction}' is the name of a country, not a capital city. Closing connection."
                conn.sendall(response.encode('utf-8'))
                break  # Close connection
            
            # OTHER COUNTRY'S CAPITAL CHECK
            matched_country = None
            for ctry, cap in countries_dict.items():
                if prediction.lower() == cap.lower():
                    matched_country = ctry
                    break
            
            # WRONG PREDICTION
            if matched_country:
                info_msg = f"'{prediction}' is the capital of {matched_country}, not {country}."
                conn.sendall(info_msg.encode('utf-8'))
            
            # Send wrong answer message
            if attempt < MAX_ATTEMPTS:
                response = f"Wrong answer. Attempts left: {MAX_ATTEMPTS - attempt}. Try again:"
            else:
                response = f"Maximum attempts reached ({MAX_ATTEMPTS}). The correct answer is {correct_capital}. Closing connection."
                print("Max attempts reached; closing connection.")
            
            conn.sendall(response.encode('utf-8'))
    
    except Exception as e:
        print(f"Error handling client: {e}")
    
    finally:
        # Close connection
        conn.close()
    
    return True

# MAIN SERVER FUNCTION
def start_server():
    """
    Starts TCP server and manages client connections.
    """

    # Load country data
    countries_dict = load_countries_data('country_capital_list.xlsx')
    
    if not countries_dict:
        print("ERROR: Could not load country data. Server cannot start.")
        return
    
    # SOCKET CREATION AND CONFIGURATION
    # AF_INET: Use IPv4
    # SOCK_STREAM: Use TCP protocol
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # SO_REUSEADDR: Allow immediate port reuse
    # (To avoid "Address already in use" error when program is restarted)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # Bind socket to specified address and port
        server_socket.bind((HOST, PORT))
        
        # Start listening (backlog=1: queue up to 1 connection at a time)
        server_socket.listen(1)
        
        print(f"Server is listening on {HOST}:{PORT}")
        print(f"Waiting for client #1 ...")
        
        # MAIN SERVER LOOP - Continuously wait for clients
        client_number = 1
        while True:
            # Wait for client connection (blocking call)
            conn, addr = server_socket.accept()
            print(f"Client connected from {addr}")
            
            # Start communication with client
            # If returns False (END command), shut down server
            should_continue = handle_client(conn, addr, countries_dict)
            
            if not should_continue:
                break
            
            # Prepare for next client
            client_number += 1
            print(f"Waiting for client #{client_number} ...")
    
    except KeyboardInterrupt:
        print("\n\nServer interrupted (Ctrl+C).")
    
    except Exception as e:
        print(f"\nServer error: {e}")
    
    finally:
        # Close server socket
        server_socket.close()

# PROGRAM ENTRY POINT
if __name__ == "__main__":
    start_server()