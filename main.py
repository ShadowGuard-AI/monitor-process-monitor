import psutil
import argparse
import logging
import sys

def setup_argparse():
    """
    Sets up the argument parser for the command-line interface.
    """
    parser = argparse.ArgumentParser(
        description="Monitor system processes for suspicious activity."
    )
    parser.add_argument(
        "-t", "--threshold",
        type=int,
        default=80,
        help="CPU usage percentage threshold to trigger an alert (default: 80%)"
    )
    parser.add_argument(
        "-i", "--interval",
        type=int,
        default=5,
        help="Interval in seconds to check processes (default: 5 seconds)"
    )
    parser.add_argument(
        "-l", "--log",
        type=str,
        default="process_monitor.log",
        help="Log file path (default: process_monitor.log)"
    )
    return parser

def main():
    """
    Main function to monitor system processes.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    if args.interval <= 0:
        print("Error: Interval must be a positive integer.")
        sys.exit(1)
    if args.threshold < 0 or args.threshold > 100:
        print("Error: Threshold must be between 0 and 100.")
        sys.exit(1)

    # Configure logging
    logging.basicConfig(
        filename=args.log,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    
    logging.info("Process Monitor Started")
    logging.info(f"Threshold: {args.threshold}%")
    logging.info(f"Interval: {args.interval} seconds")
    
    seen_pids = set()
    alerted_pids = set()

    try:
        while True:
            current_pids = set()
            for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent']):
                try:
                    pid = proc.info['pid']
                    current_pids.add(pid)
                    if pid not in seen_pids:
                        # The first cpu_percent reading for a process is a
                        # priming reading with no meaning, so a newly seen
                        # process is primed here and can only alert from
                        # its next cycle.
                        seen_pids.add(pid)
                        continue
                    cpu_usage = proc.info['cpu_percent']
                    if cpu_usage > args.threshold:
                        if pid not in alerted_pids:
                            alerted_pids.add(pid)
                            logging.warning(
                                f"High CPU Usage Detected - PID: {pid}, "
                                f"Name: {proc.info['name']}, CPU: {cpu_usage}%"
                            )
                    else:
                        alerted_pids.discard(pid)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            seen_pids.intersection_update(current_pids)
            alerted_pids.intersection_update(current_pids)
            psutil.time.sleep(args.interval)
    except KeyboardInterrupt:
        logging.info("Process Monitor Stopped by User")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()