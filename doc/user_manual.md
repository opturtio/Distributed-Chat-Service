# User Manual

To run this project, you need to add the IP address and the port of both the node itself and the leader node it will connect to. To do this, you will need to create a .env file inside the src folder, and add the following values:

```
(Note that these are example values, you will need to check the real values yourself)

peer_host = "0.0.0.0"
peer_port = 8000
peer_host_own = "0.0.0.0"
peer_port_own = 8000

```

## Development Commands

### Create virtual environment:
```
python3 -m venv venv
```

### Activate virtual environment:
```bash
source venv/bin/activate
```

### Deactivate virtual environment:
```bash
deactivate
```

### Run the program in src-folder:
```bash
python3 main.py
```

### Add requirement library:
```bash
pip install python-dotenv
```

