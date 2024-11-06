# Installation Guide

### Clone the project:
```bash
git clone git@github.com:opturtio/Distributed-Chat-Service.git
```

### Go to repository:
```bash
cd Distributed-Chat-Service
```

### Install virtual environment:
```bash
python3 -m venv venv
```

### Start virtual environment:
```bash
source venv/bin/activate
```

### Install requirements:
```bash
pip install -r requirements.txt
```

### Create .env-file:
```bash
touch .env
```

### Generate and add the secret key to the .env file:
```bash
python3 -c "import secrets; print(f'SECRET_KEY={secrets.token_hex(64)}')" >> .env
```

**Example .env-file:**
```python
SECRET_KEY=18fd24bf6a2ad4dac04a33963db1c42f
```
