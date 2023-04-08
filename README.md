# iq-brain-ai

Custom library used for own purpose.

## Installation

1. Install venv for local development
    ```bash
    python3 -m venv venv
    ```
    This will create venv folder for installing environment for local development purpose 
2. Check python
    ```bash
    which python
    ```
    if you don't see $MODULE_DIR/venv/bin/python
    Try this
    ```bash
    source venv/bin/activate
    ```
3. Install dependencies
    ```bash
    pip3 install -r requirements.txt
    ```
4. Bring up postgres docker db 
    ```bash
    docker-compose up -d
    ```
   This will create postgres db with username/password/database defined in docker-compose.yml file
5. Create .env file
   1. Go to config/template.env
   2. Copy to the same directory as .env
   3. double check username/password/database/port which is setup in docker-compose file

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Author
[Vignesh Sellamuthu](https://www.linkedin.com/in/vsks/)