# OHLC Data Generator and Metric Enrichment

This project generates simulated OHLC (Open, High, Low, Close) data for a fictional stock, aggregates it into various time frames, and enriches it with financial metrics. The application is Dockerized for consistent environment setup and execution.

## Features

*   **OHLC Data Generation**: Simulates 1-minute OHLC bar data for a trading day (9:30 AM - 4:00 PM).
*   **Data Aggregation**: Aggregates 1-minute bars into 5-minute, 30-minute, and daily bars.
*   **Metric Enrichment**: Calculates 30-minute Moving Average, 30-minute Moving Median, and Volume Weighted Average Price (VWAP) for aggregated data.
*   **Dockerized Environment**: Ensures easy setup and consistent execution.
*   **Configurable Settings**: Parameters are customizable via `trading_settings.yaml`.

## Getting Started

### Prerequisites

Ensure you have [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/) installed.

### Running the Application

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/kobonable/home_task_from_bullettech.git
    cd home_task_from_bullettech
    ```
    (Replace `https://github.com/your-username/ohlc_driver.git` with the actual repository URL if different.)

2.  **Build and run the Docker containers:**
    ```bash
    docker-compose up --build
    ```
    This command will build the Docker images and start the services.

### Viewing Results

Processed data will be saved in the `result_data/` directory, which is volume-mounted to your host machine. You can access these files directly in your project's `result_data/` folder:

```bash
ls result_data/
```

### Stopping the Application

To stop running containers, press `Ctrl+C` in the terminal where `docker-compose up` is running. To stop and remove containers, networks, and volumes:

```bash
docker-compose down
```

## Project Structure

*   [`Dockerfile`](Dockerfile): Defines the Docker image.
*   [`docker-compose.yml`](docker-compose.yml): Orchestrates Docker containers.
*   [`main.py`](main.py): Main entry point for data generation and processing.
*   [`ohlc_generator.py`](ohlc_generator.py): Script for generating 1-minute OHLC data.
*   [`ohlc_metrics_enrichment.py`](ohlc_metrics_enrichment.py): Script for aggregating data and calculating metrics.
*   [`requirements.txt`](requirements.txt): Python dependencies.
*   [`trading_settings.yaml`](trading_settings.yaml): Configuration file.
*   [`result_data/`](result_data/): Directory for output data files.
*   [`tests/`](tests/): Unit tests.

## Configuration

Adjust data generation and metric calculation parameters in [`trading_settings.yaml`](trading_settings.yaml).

## Running Tests

From the project root, use Docker Compose to run tests:

```bash
docker-compose exec ohlcdriver pytest tests/
