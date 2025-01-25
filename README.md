# fftp

⚡️ flash ftp (fftp). Quickly bootstrap an ftp server


## Installation

Prerequisites
- Python 3
- [pipx](https://github.com/pypa/pipx) or [pip](https://github.com/pypa/pip)

```bash
pipx install .
```

Alternative:

```bash
pip install -r requirements.txt .
pip install .
```

## Usage

```bash
usage: fftp [-h] --dir DIR [--port PORT]

Temporary FTP Server

options:
  -h, --help            show this help message and exit
  --dir DIR, -d DIR     Directory to serve files from
  --port PORT, -p PORT  Port to run the FTP server o
```

**Example**
```bash
python3 fftp.py --dir . --port 2121
```
