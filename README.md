# Threat Intelligence FastAPI

This project is a simple FastAPI-based web service designed for threat intelligence purposes. It provides an API to collect and serve threat data efficiently. The service also has a simple auth mechanism.

## Installation Guide

### Prerequisites

Ensure you have the following installed:

- Python (>=3.13)
- [Poetry](https://python-poetry.org/docs/#installation)
- Git
- Docker

### Clone the Repository

```bash
git clone https://github.com/AliHezarpisheh/threat-intelligence-fastapi.git
cd threat-intelligence-fastapi
```

### Install Dependencies

This project uses Poetry for dependency management, with different groups for main, development, and testing dependencies.

1. Install the main dependencies:

    ```bash
    poetry install --without dev,test
    ```

2. If you are working in a development environment, install dev dependencies as well:

    ```bash
    poetry install --with dev
    ```

3. If you need to run tests, install test dependencies:

    ```bash
    poetry install --with test
    ```

### Running the Application

To start the FastAPI application in the development mode:

```bash
source .venv/bin/activate
fastapi dev
```

This runs the service with live reloading for development purposes.
