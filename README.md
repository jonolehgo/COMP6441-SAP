# COMP6441: Something Awesome Project 🚩

A project to showcase how SQLi is utlised to obtain secret infromation. This application consists of 3 CTF (Capture The Flag) challenges:

1. Obtain secret user (within a single table)
2. Obtain secret location (within another table [requires multilple queries])
3. Set blog title (using both select and insert queries)

## Table of contents

- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Creators](#creators)
- [Thanks](#thanks)

## Requirements

You will need to install the requirements and set up your own database.

```
pip install -r requirements.txt
```

Then in the root directory create a file named 'credentials.py' and replace the values with your credentials.

```
db_credentials = {
    "database": "<YOUR_DATABASE_NAME>",
    "host": "localhost",
    "user": "<YOUR_DATABASE_USERNAME>",
    "password": "<YOUR_DATABASE_USERNAME>",
    "port": "<YOUR_DATABASE_PORT>"
}

```

## Quick Start

```
uvicorn server:app --reload
```

```
streamlit run app.py
```

## Creators

**Jonathan Tea**

- <https://github.com/jonolehgo>

## Thanks

This project is in asscociation with The University of New South Wales (COMP6441).
