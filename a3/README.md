# CS 158A - Assignment 3: Leader Election in a Ring

This project implements the Leader Election algorithm for an asynchronous ring topology. Each node in the ring communicates with its neighbors to elect the process with the highest ID as the leader.

---
## Files Included

* `myleprocess.py`: The Python script for a single node in the election ring.
* `config.txt`: The configuration file specifying the node's server port and its neighbor's port.
* `README.md`: This setup and execution guide.

---
## How to Run the 3-Node Demo

### Prerequisites
* Python 3.x

### Execution
To simulate a 3-node ring, you must open **three separate terminal windows**. You will need to **change the contents of `config.txt`** before launching each process to form the ring.

**Step 1: Launch Process 1**

1.  Ensure `config.txt` has the following content (Server: 5001, Neighbor: 5002):
    ```
    127.0.0.1,5001
    127.0.0.1,5002
    ```
2.  In your **first terminal**, run:
    ```bash
    python myleprocess.py log1.txt
    ```

**Step 2: Launch Process 2**

1.  **Immediately** change the content of `config.txt` (Server: 5002, Neighbor: 5003):
    ```
    127.0.0.1,5002
    127.0.0.1,5003
    ```
2.  In your **second terminal**, run:
    ```bash
    python myleprocess.py log2.txt
    ```

**Step 3: Launch Process 3**

1.  **Immediately** change the content of `config.txt` one last time (Server: 5003, Neighbor: 5001):
    ```
    127.0.0.1,5003
    127.0.0.1,5001
    ```
2.  In your **third terminal**, run:
    ```bash
    python myleprocess.py log3.txt
    ```

The processes will connect, and after a short time, each terminal will announce the same leader ID.

### Stopping the Program
To stop all processes, press **`Ctrl+C`** in each terminal. This will trigger a graceful shutdown and ensure all network connections are closed cleanly.
