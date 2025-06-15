# Secure File Integrity Monitor

A Python tool to monitor directories for file changes and verify integrity using SHA-256 hashes. Sends alerts via email on suspicious activity. Catch the bad guys when they are doing....bad things! Simple tool, but I like to think of it as elegant.  

## Features
- Detects file creation, modification, and deletion
- Uses cryptographic hashes for integrity checking
- Email alerting support
- Easy configuration via YAML

## Usage

1. Clone the repo and install dependencies:
    ```
    pip install -r requirements.txt
    ```
2. Edit `config.yaml` with your settings.
3. Run the monitor:
    ```
    python monitor.py
    ```

## Security Best Practices

- Store sensitive credentials securely (use environment variables or secrets manager in production).
- Run with least privilege.

## License

MIT
