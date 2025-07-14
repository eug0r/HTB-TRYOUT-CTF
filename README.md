```markdown
# Dynamic Paths Solver: Optimized for Efficiency (and Minimal Existential Dread)

Welcome to the documentation for the `Dynamic Paths Solver`. If you're here, you're likely dealing with a grid-based pathfinding problem, or perhaps just trying to automate something that feels like a particularly aggressive game of "follow the numbers." Either way, this solution aims to reduce your computational (and emotional) burden.

---

## The Problem: Grid Traversal with Constraints

The core challenge involves navigating a 2D grid, where each cell contains a numerical 'cost'. Your objective is to find the path from the top-left cell (source) to the bottom-right cell (destination) that yields the minimum total sum of costs. The only permissible movements are **down** or **right**.

**Input Format:**

The server provides dimensions `i j` (rows and columns), followed by a space-separated list of `n_i,j` values representing the flattened grid.

**Example Input:**

```

4 3
2 5 1 9 2 3 9 1 3 11 7 4

```

This input translates to the following grid structure:

```

2  5  1
9  2  3
9  1  3
11 7  4

````

The expected output is a single integer: the minimum sum of costs along the optimal path. For the example above, the optimal sum is `17`. (Yes, we verified it. You're welcome.)

---

## The Solution: Dynamic Programming (Because Recursion Alone is for Amateurs)

This problem is a textbook candidate for **Dynamic Programming**. Why? Because the optimal solution for a given cell depends directly on the optimal solutions of its immediate predecessors. Re-calculating these values would be, frankly, inefficient.

The approach is straightforward:

1.  **DP Table Initialization:** Construct a 2D array (let's call it `dp`) of identical dimensions to the input grid. Each `dp[r][c]` entry will store the minimum cumulative cost to reach cell `(r, c)` from the starting point `(0, 0)`.

2.  **Base Case:** The cost to reach the starting cell `(0, 0)` is simply its own value: `dp[0][0] = grid[0][0]`. No complex decisions here, thankfully.

3.  **Boundary Conditions:**
    * For any cell in the first row (`r = 0, c > 0`), the only valid preceding cell is `(0, c-1)`. Therefore, `dp[0][c] = dp[0][c-1] + grid[0][c]`.
    * Similarly, for any cell in the first column (`c = 0, r > 0`), the only valid preceding cell is `(r-1, 0)`. Thus, `dp[r][0] = dp[r-1][0] + grid[r][0]`.

4.  **General Recurrence Relation:** For all other cells `(r, c)` where `r > 0` and `c > 0`, the minimum cost to reach `(r, c)` is the minimum of the costs from the cell directly above (`dp[r-1][c]`) and the cell directly to the left (`dp[r][c-1]`), plus the cost of the current cell `grid[r][c]`.
    ```
    dp[r][c] = min(dp[r-1][c], dp[r][c-1]) + grid[r][c]
    ```
    *In simpler terms: `dp[r][c]` is the current cell's value plus the minimum cost to reach either the cell above it or the cell to its left.*

5.  **Final Result:** The minimum total cost to traverse the grid will be found in the bottom-right cell of the DP table: `dp[rows-1][cols-1]`. Your final answer.

---

## The Code: Your Automated Grid-Solving Assistant

The provided Python script (`solver.py`) encapsulates this logic and automates the interaction with the challenge server. Because manual input for 100 test cases is a form of torture we aim to avoid.

### Technical Overview:

* **`socket` Module:** This is the standard Python library for network communication. It establishes a TCP connection to the challenge server, allowing for bidirectional data exchange. It handles the low-level complexities so you don't have to.

* **`solve_grid(grid_data)` Function:**
    * Receives a list containing grid dimensions and flattened values.
    * Reconstructs the 2D grid from the flattened input.
    * Implements the dynamic programming algorithm described above to compute the minimum path sum.
    * Returns the final calculated minimum sum.

* **`read_until_prompt(sock, prompt="> ")` Function:**
    * A utility function designed to robustly read incoming data from the socket.
    * It continuously receives chunks of data until a specified `prompt` string (e.g., `"> "`) is detected, ensuring that a complete problem description is captured before parsing. This avoids issues with partial reads common in socket programming.

* **`main()` Function:**
    * Initializes the socket connection to the specified `HOST` and `PORT`.
    * Performs an initial read to consume any introductory server messages or example data, up to the first prompt.
    * Enters a loop to process 100 distinct test cases:
        1.  Parses the dimensions and grid values from the received data block. Robust error handling is included for malformed input.
        2.  Invokes `solve_grid()` to determine the minimum path sum for the current grid.
        3.  Encodes and transmits the calculated sum back to the server, followed by a newline character.
        4.  Reads the next problem statement from the server, awaiting the subsequent prompt, and continues the loop.
    * Upon completion of all tests, it attempts to read any final server responses (e.g., the challenge flag).

### Execution Instructions:

1.  **Save:** Store the Python code as `solver.py`.
2.  **Navigate:** Open your terminal or command prompt and change your directory to where `solver.py` is saved.
3.  **Run:** Execute the script using `python solver.py`.
4.  **Monitor:** Observe the terminal output. The script will print its connection status, the test number being processed, the calculated sum, and the data sent. A successful run concludes with a message indicating all tests are completed.

**Note on Robustness:** Network communication can be unpredictable. The `read_until_prompt` function and error handling are designed to mitigate common issues like partial data reception or unexpected input formats. However, slight variations in server behavior (e.g., different prompts, unannounced disconnections) might necessitate minor adjustments to the parsing logic. It's a delightful dance between your code and the server's whims.
````
