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
    
    # Configure logging
    logging.basicConfig(
        filename=args.log,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    
    logging.info("Process Monitor Started")
    logging.info(f"Threshold: {args.threshold}%")
    logging.info(f"Interval: {args.interval} seconds")
    
    try:
        while True:
            for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent']):
                try:
                    cpu_usage = proc.info['cpu_percent']
                    if cpu_usage > args.threshold:
                        logging.warning(
                            f"High CPU Usage Detected - PID: {proc.info['pid']}, "
                            f"Name: {proc.info['name']}, CPU: {cpu_usage}%"
                        )
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            psutil.time.sleep(args.interval)
    except KeyboardInterrupt:
        logging.info("Process Monitor Stopped by User")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()