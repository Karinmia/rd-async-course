## Development of sync/async HTTP web services and their comparison.

## Prerequisites

We will perform load testing of our HTTP services, therefore we need to install some tools for that.
You can choose between:

- [Apache Benchmark](https://httpd.apache.org/docs/current/programs/ab.html)

- Hey ([Installation instructions](https://github.com/rakyll/hey?tab=readme-ov-file#installation))

## Setup

1. Setup your virtual environment and install dependencies:

   ```shell
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```


# Load Testing Results

This document presents the performance metrics of different HTTP services implemented using WSGI, ASGI, Starlette, and FastAPI. Each service was tested with various configurations, including different numbers of workers and varying delay times for the requests.

## Test Configuration
- **Services:** WSGI, ASGI, Starlette, FastAPI
- **Workers:** 1, 5, 10
- **Delay Times:** 2 seconds, 1 second, 0.5 seconds, 50ms
- **Machine Specs:** 10 CPU cores (M2 Pro)

## Results

### 2-Second Delay

| Workers | Metric         | WSGI  | ASGI  | Starlette | FastAPI |
|---------|----------------|-------|-------|-----------|---------|
| 1       | Total Time (secs) | 86.0216   | 56.0844  | 53.8693  | 54.1808  |
|         | Slowest (secs)    | 18.0375   | 5.7320   | 3.3572   | 3.4816   |
|         | Fastest (secs)    | 2.0091    | 2.5072   | 2.5047   | 2.5061   |
|         | Average (secs)    | 10.0233   | 2.7492   | 2.6089   | 2.5887   |
|         | Requests/sec      | 0.4999    | 3.5661   | 3.7127   | 3.6913   |
| 5       | Total Time (secs) | 105.0438  | 54.234   | 52.8304  | 53.3902  |
|         | Slowest (secs)    | 5.9748    | 5.7175   | 3.5450   | 3.5112   |
|         | Fastest (secs)    | 2.5844    | 2.5072   | 2.5072   | 2.5041   |
|         | Average (secs)    | 5.1180    | 2.6555   | 2.5969   | 2.6157   |
|         | Requests/sec      | 1.9040    | 3.6877   | 3.7857   | 3.7460   |
| 10      | Total Time (secs) | 54.6828   | 56.0905  | 56.4029  | 53.4605  |
|         | Slowest (secs)    | 3.9333    | 5.7797   | 5.2682   | 3.8203   |
|         | Fastest (secs)    | 2.5057    | 2.5066   | 2.5066   | 2.5076   |
|         | Average (secs)    | 2.6553    | 2.7533   | 2.6753   | 2.5882   |
|         | Requests/sec      | 3.6575    | 3.5657   | 3.5459   | 3.7411   |
