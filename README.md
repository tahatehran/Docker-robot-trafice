# robot trafice

The **Request Simulator** is a Python-based application designed to simulate multiple HTTP requests to a list of URLs. It uses `aiohttp` for asynchronous HTTP requests and supports customizable user agents for different browsers and operating systems. The application logs the results of each request and saves them to a JSON file for further analysis.

---

## Features

- **Asynchronous Requests**: Uses `aiohttp` to send multiple HTTP requests concurrently.
- **Custom User Agents**: Supports predefined user agents for various browsers and operating systems.
- **Dynamic URL Loading**: Loads URLs from a `list.txt` file, which can be updated dynamically.
- **Logging**: Logs request results to `request_log.txt` and saves detailed results to `login.json`.
- **Docker Support**: Easily containerized with Docker and Docker Compose for consistent deployment.

---

## Prerequisites

Before running the application, ensure you have the following installed:

- **Python 3.9+**
- **Docker** (optional, for containerized deployment)
- **Docker Compose** (optional, for containerized deployment)

---

## Installation

### 1. Clone the Repository

```bash
git clone git@github.com:tahatehran/Docker-robot-trafice.git
cd Docker-robot-trafice
````
### 2.Set Up the Environment

#### Option 1: Run Locally (Without Docker)

1. Install the required Python dependencies using the `requirements.txt` file. This file contains all the necessary libraries for running the application.

2. Create a file named `list.txt` in the root of the project. Add the URLs you want to send requests to, with each URL on a separate line. For example:

```bash
https://example.com
````

3. Run the application using the appropriate command. This will start sending requests to the URLs listed in `list.txt`.

#### Option 2: Run with Docker

1. If you want to run the application using Docker, ensure that Docker and Docker Compose are installed on your system.

2. Use Docker Compose to build and run the application. This will automatically create an isolated environment for running the application.

3. If you want the application to run in the background, you can use Detached mode. This allows the application to continue running without keeping the terminal open.

4. To stop the application, use the appropriate command. This will stop and remove all containers associated with the application.
