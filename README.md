# Port Scanner — Phase 1
**Course:** 605346 Information & Network Security Programming  
**University of Petra**

---

## Overview

A Python command-line tool that scans a target IP address for open TCP ports using multithreading. Multiple ports are scanned concurrently using `ThreadPoolExecutor`, and all results are saved to a timestamped log file.

---

## Requirements

- Python 3.x
- No external libraries needed (all imports are from the Python standard library)

---

## How to Run

```
python3 port_scanner.py --target <IP> --ports <start-end> --threads <number>
```

### Examples

Scan ports 1 to 1024 on your own machine:
```
python3 port_scanner.py --target 127.0.0.1 --ports 1-1024 --threads 50
```

Scan a specific range with fewer threads:
```
python3 port_scanner.py --target 192.168.1.1 --ports 20-80 --threads 10
```

### Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--target` | Yes | — | IP address to scan |
| `--ports` | No | 1-1024 | Port range in format start-end |
| `--threads` | No | 50 | Number of concurrent threads |

---

## Output

The tool prints open ports to the terminal and saves all results (open and closed) to a timestamped text file:

```
scan_results_2025-04-16_14-30-00.txt
```

Example log file content:
```
Port Scan Results
Target : 127.0.0.1
Ports  : 1-1024
Threads: 50
Started: 2025-04-16 14:30:00
----------------------------------------
[2025-04-16 14:30:01] [ThreadPoolExecutor-0_0] Port 22: OPEN
[2025-04-16 14:30:01] [ThreadPoolExecutor-0_1] Port 80: CLOSED
...
----------------------------------------
Scan finished: 2025-04-16 14:30:05
```

---

## Design Decisions

### Multithreading with ThreadPoolExecutor
Instead of scanning ports one by one (which would be very slow), the tool uses `ThreadPoolExecutor` to scan many ports at the same time. Each thread picks up one port, runs the scan, and writes the result.

### Thread Safety with Lock
Since multiple threads write to the same log file at the same time, a `threading.Lock()` is used. Before writing, a thread acquires the lock — other threads wait until it is released. This prevents corrupted or overlapping log entries.

### Socket Connection
Each port is tested using `socket.connect_ex()`. If the return value is `0`, the connection was successful and the port is open. Any other value means the port is closed or filtered.

### Timestamped Logging
Every log entry includes the current timestamp and the thread name, making it easy to trace which thread scanned which port and when.

---

## File Structure

```
port-scanner-phase1/
├── port_scanner.py   # Main tool
└── README.md         # This file
```
