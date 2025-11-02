#-----------------------------------------------------
# Title: Country Capital Prediction Client
# Author: Abdullah Esin
# ID: ************
# Section: 3
# Assignment: 1
# Description: This client implements a TCP socket-based client for the country 
#              capital prediction application. It connects to the server, receives 
#              questions about country capitals, sends user predictions, and 
#              displays server responses. The client handles various application states 
#              including correct answers, wrong attempts with remaining chances, 
#              and graceful session termination with the END command.
#-----------------------------------------------------

import socket

# CONSTANTS AND CONFIGURATION
HOST = '127.0.0.1'  # Server address (localhost)
PORT = 65432        # Port number the server listens on
BUFFER_SIZE = 1024  # Buffer size for receiving data

# MAIN CLIENT FUNCTION
def start_client():
    """
    Starts TCP client and establishes communication with server.
    """
    
    # SOCKET CREATION AND CONNECTION TO SERVER
    # AF_INET: Use IPv4
    # SOCK_STREAM: Use TCP protocol
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to server
        client_socket.connect((HOST, PORT))
        
        # RECEIVE FIRST MESSAGE
        data = client_socket.recv(BUFFER_SIZE)
        if not data:
            print("Server closed connection without sending question.")
            return
        # Decode and print question from server
        question = data.decode('utf-8')
        print(question)
        # MAIN COMMUNICATION LOOP
        while True:
            # GET USER INPUT
            user_input = input().strip()
            # Empty input check
            if not user_input:
                print("Please enter a valid guess or 'END'.")
                continue
            # SEND PREDICTION TO SERVER
            try:
                client_socket.sendall(user_input.encode('utf-8'))
            except Exception as e:
                print(f"Error sending data: {e}")
                break
            
            # RECEIVE RESPONSE FROM SERVER
            response_text = None
            try:
                response = client_socket.recv(BUFFER_SIZE)
                if not response:
                    print("Server closed connection.")
                    break
                
                response_text = response.decode('utf-8')
                print(response_text)
                
            except Exception as e:
                print(f"Error receiving data: {e}")
                break
            
            # Check response if we successfully received it
            if response_text is None:
                break
            
            if "Correct!" in response_text:
                break
            elif "Session ended by client. Goodbye." in response_text:
                break
            # WRONG ANSWER - Still has attempts left
            elif "Wrong answer. Attempts left:" in response_text:
                # Loop continues, ask user for new prediction
                continue
            # ANOTHER COUNTRY'S CAPITAL - Info message + wrong message will come
            elif "is the capital of" in response_text:
                # Receive next message from server (wrong message)
                try:
                    next_response = client_socket.recv(BUFFER_SIZE)
                    if next_response:
                        next_text = next_response.decode('utf-8')
                        print(next_text)
                        
                        # If still has attempts, continue
                        if "Wrong answer. Attempts left:" in next_text:
                            continue
                        else:
                            break
                except:
                    break
            # COUNTRY NAME ENTERED - Connection should terminate
            elif "is the name of a country" in response_text:
                break
            # NUMERIC INPUT - Connection should terminate
            elif "Numeric input is not allowed" in response_text:
                break
            # Maximum attempts or other final messages
            elif "Maximum attempts reached" in response_text:
                break
            else:
                break
    
    except ConnectionRefusedError:
        print(f"ERROR: Could not connect to server at {HOST}:{PORT}")
        print("Make sure the server is running first.")
    
    except Exception as e:
        print(f"ERROR: {e}")
    
    finally:
        # CLOSE CONNECTION
        client_socket.close()

# PROGRAM ENTRY POINT
if __name__ == "__main__":
    start_client()