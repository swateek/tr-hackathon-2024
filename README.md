# TR Hackathon 2024

### Getting Started

1. Create a virtual environment
```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --no-cache -r pip-requirements.txt
```

2. For the examples

```bash
    cd examples
    touch .config.ini

    # add the lines below, without the #
    # [DEFAULT]
    # AWS_DEFAULT_REGION=us-west-2
    # AWS_ACCESS_KEY_ID=valuewithnoquotes
    # AWS_SECRET_ACCESS_KEY=valuewithnoquotes
    # AWS_SESSION_TOKEN=valuewithnoquotes
```
