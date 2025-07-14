import socket
import time # For potential small delays if needed

def solve_grid(grid_data):
    """
    Solves a single grid to find the minimum path sum.
    grid_data: a list of integers representing the flattened grid.
    """
    rows, cols = grid_data[0], grid_data[1]
    flat_values = grid_data[2:]

    # Reconstruct the grid
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    k = 0
    for r in range(rows):
        for c in range(cols):
            grid[r][c] = flat_values[k]
            k += 1

    # Initialize DP table
    dp = [[0 for _ in range(cols)] for _ in range(rows)]

    # Base case
    dp[0][0] = grid[0][0]

    # Fill first row
    for c in range(1, cols):
        dp[0][c] = dp[0][c-1] + grid[0][c]

    # Fill first column
    for r in range(1, rows):
        dp[r][0] = dp[r-1][0] + grid[r][0]

    # Fill the rest of the DP table
    for r in range(1, rows):
        for c in range(1, cols):
            dp[r][c] = min(dp[r-1][c], dp[r][c-1]) + grid[r][c]

    return dp[rows-1][cols-1]

def read_until_prompt(sock, prompt="> "):
    """Reads from the socket until the specified prompt is found."""
    buffer = ""
    while True:
        try:
            chunk = sock.recv(4096).decode('utf-8', errors='ignore')
            if not chunk:
                print("Server closed connection prematurely.")
                return None
            buffer += chunk
            if prompt in buffer:
                # Return everything up to and including the prompt
                return buffer
        except UnicodeDecodeError:
            print("UnicodeDecodeError during socket read. Ignoring error.")
            continue # Try to read more
        except socket.timeout: # Add a timeout for debugging if needed
            print("Socket timeout during read.")
            return None


def main():
    HOST = '94.237.50.221'
    PORT = 56021

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Connected to {HOST}:{PORT}")

        # --- Initial Read: Consume all introductory text ---
        print("Reading initial server message...")
        initial_message = read_until_prompt(s, prompt="> ") # The first prompt is after examples
        if initial_message is None:
            return
        print(f"Initial message received:\n{initial_message}")

        # Now, the first actual "Test 1/100" should be ready after we send the first answer.
        # However, the example output shows that "Test 1/100" *is* part of that initial message
        # before the first "> ". So we need to parse it from the initial_message.

        # Let's re-evaluate based on your output:
        # Received raw data:
        #
        #            11 7 4
        #
        # Example Response:
        #            17
        # (Optimal route is 2 -> 5 -> 2 -> 1 -> 3 -> 4)
        #
        # Test 1/100
        # 5 2
        # 3 6 7 7 7 8 3 5 5 2
        # >

        # This implies that the 'read_until_prompt' correctly got *everything*
        # up to the first "> ". So `initial_message` now contains Test 1.
        # We need to process this `initial_message` to get the first grid.

        # The loop will then handle subsequent tests.

        current_test_data = initial_message # The first test is in the initial_message
        
        for test_num in range(1, 101): # 100 tests
            print(f"\n--- Processing Test {test_num}/100 ---")

            lines = current_test_data.strip().split('\n')
            
            # Find the actual start of the test data
            grid_start_idx = -1
            for i, line in enumerate(lines):
                if line.strip().startswith(f"Test {test_num}/100"):
                    grid_start_idx = i
                    break

            if grid_start_idx == -1:
                print(f"Error: Could not find 'Test {test_num}/100' marker in received input.")
                print(f"Received data:\n{current_test_data}")
                return

            # Extract relevant lines for the grid, after the "Test X/100" line
            # and before the ">" prompt.
            grid_lines_raw = []
            for i in range(grid_start_idx + 1, len(lines)):
                line = lines[i].strip()
                if line.startswith('>') or not line: # End of grid data, or empty line
                    break
                grid_lines_raw.append(line)
            
            if len(grid_lines_raw) < 2:
                print(f"Error: Not enough lines for grid data (dimensions + values) for Test {test_num}.")
                print(f"Extracted grid lines raw: {grid_lines_raw}")
                print(f"Full received data:\n{current_test_data}")
                return

            try:
                dims = list(map(int, grid_lines_raw[0].split()))
                rows, cols = dims[0], dims[1]
                flat_values = list(map(int, grid_lines_raw[1].split()))
            except (IndexError, ValueError) as e:
                print(f"Error parsing grid dimensions or values for Test {test_num}: {e}")
                print(f"Lines: {grid_lines_raw}")
                return

            # Validate data length
            expected_len = rows * cols
            if len(flat_values) != expected_len:
                print(f"Error: Mismatch in grid data length for Test {test_num}. Expected {expected_len}, got {len(flat_values)}")
                print(f"Dimensions: {rows}x{cols}, Values: {flat_values}")
                return

            # Prepare data for solve_grid
            grid_input_for_func = [rows, cols] + flat_values
            
            # Solve the grid
            min_sum = solve_grid(grid_input_for_func)
            print(f"Calculated minimum sum: {min_sum}")

            # Send the answer back, followed by a newline
            s.sendall(str(min_sum).encode('utf-8') + b'\n')
            print(f"Sent: {min_sum}")

            # Read the next challenge. This read *should* get the next "Test X/100"
            # and its associated grid data, up to the next "> " prompt.
            if test_num < 100: # Only read for the next test if not the last one
                current_test_data = read_until_prompt(s, prompt="> ")
                if current_test_data is None:
                    print(f"Failed to read data for Test {test_num + 1}.")
                    return
                #print(f"Received raw data for next test:\n{current_test_data}") # For debugging
            else:
                print("All tests sent. Waiting for final server response/flag...")
                # Read any final messages from the server, like a flag.
                final_response = read_until_prompt(s, prompt="") # Read until server closes or timeout
                if final_response:
                    print(f"Final server response:\n{final_response}")

        print("\nAll 100 tests completed.")

if __name__ == "__main__":
    main()
