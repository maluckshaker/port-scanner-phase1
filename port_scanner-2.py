import socket
import threading
import argparse
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

file_lock = threading.Lock()

def scan_port(target, port, log_file):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        sock.close()

        if result == 0:
            status = "OPEN"
        else:
            status = "CLOSED"

    except socket.error:
        status = "ERROR"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    thread_name = threading.current_thread().name
    message = f"[{timestamp}] [{thread_name}] Port {port}: {status}\n"

    with file_lock:
        with open(log_file, "a") as f:
            f.write(message)

    if status == "OPEN":
        print(f"  [OPEN]  Port {port}")


def main():
    parser = argparse.ArgumentParser(description="Multithreaded Port Scanner")
    parser.add_argument("--target",  required=True,        help="Target IP address")
    parser.add_argument("--ports",   default="1-1024",     help="Port range (e.g. 1-1024)")
    parser.add_argument("--threads", type=int, default=50, help="Number of threads")
    args = parser.parse_args()

    start_port, end_port = map(int, args.ports.split("-"))
    port_list = list(range(start_port, end_port + 1))

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = f"scan_results_{timestamp}.txt"

    with open(log_file, "w") as f:
        f.write(f"Port Scan Results\n")
        f.write(f"Target : {args.target}\n")
        f.write(f"Ports  : {args.ports}\n")
        f.write(f"Threads: {args.threads}\n")
        f.write(f"Started: {datetime.now()}\n")
        f.write("-" * 40 + "\n")

    print(f"\nScanning {args.target} on ports {args.ports} using {args.threads} threads...")
    print(f"Results will be saved to: {log_file}\n")

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        for port in port_list:
            executor.submit(scan_port, args.target, port, log_file)

    with open(log_file, "a") as f:
        f.write("-" * 40 + "\n")
        f.write(f"Scan finished: {datetime.now()}\n")

    print(f"\nScan complete! Full results saved to: {log_file}")


if __name__ == "__main__":
    main()
