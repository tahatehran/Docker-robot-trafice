# Request Simulator

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
git clone https://github.com/your-username/request-simulator.git
cd request-simulator

