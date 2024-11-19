# Installation Guide

**Prerequisite: PostgreSQL must be installed and running on your system.**

### Clone the Project:
```bash
git clone git@github.com:opturtio/Distributed-Chat-Service.git
```

### Navigate to the Project Directory:
```bash
cd Distributed-Chat-Service
```

### Set Up a Virtual Environment:
```bash
python3 -m venv venv
```

### Activate the Virtual Environment:
```bash
source venv/bin/activate
```

### Install Dependencies:
```bash
pip install -r requirements.txt
```

### Create an .env-file:
```bash
touch .env
```

### Generate and Add the Secret Key to the .env file:
```bash
python3 -c "import secrets; print(f'SECRET_KEY={secrets.token_hex(64)}')" >> .env
```

### Add Database URL to .env-file:
```bash
echo 'DATABASE_URL=postgresql:///user' >> .env
```

### Create the Database:
```bash
psql -U postgres -d user < schema.sql
```

**Example .env-file:**
```python
DATABASE_URL=postgresql:///user
SECRET_KEY=18fd24bf6a2ad4dac04a33963db1c42f
```
