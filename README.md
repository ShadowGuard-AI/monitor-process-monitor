![Banner](banner.png)

## Monitor Process Monitor

### Project Description

This tool aims to enhance cybersecurity by monitoring system processes for suspicious activity. It is designed to detect and alert on anomalous process behavior that could indicate a potential threat. The focus is on system monitoring and proactive alerting, empowering users to swiftly mitigate potential risks.

### Installation

Clone this repository, then install the tool's only third-party dependency:

```
pip install psutil
```

(The repository ships no requirements.txt; `psutil` is the only import in main.py that is not part of the Python standard library.)

### Usage Examples

```bash
# Run the tool with default arguments
python main.py

# Run the tool with custom arguments (check every 60 seconds, log to log.txt)
python main.py --interval 60 --log log.txt
```

Options: `-t` / `--threshold` sets the CPU usage percentage that triggers an alert (default 80), `-i` / `--interval` sets the seconds between checks (default 5), and `-l` / `--log` sets the log file path (default process_monitor.log).

The interval must be above 0 and the threshold must be between 0 and 100; any other value is refused at startup with exit 1. The first CPU reading for a newly seen process only primes its measurement, so a process can alert on CPU only from the second cycle in which it is observed. A process that stays over the threshold is warned about once, and again only after it has dropped below the threshold and crossed it again.

### Security Warnings

This tool is solely intended to enhance system security and should only be used for legitimate purposes. Any unauthorized or malicious use of this tool is strictly prohibited.

### License

This tool is licensed under the GNU General Public License v3.0 and is licensed to CY83R-3X71NC710N.