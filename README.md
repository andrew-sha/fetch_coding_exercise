# Fetch Coding Exercise

This is a simple REST API service that facilitates the adding, spending, and viewing of points acquired through multiple payers for a single user.

## Functionality

The API supports the following endpoints:
- **/add (POST)**: Grant the user points for a specific payer at a given timestamp.
- **/spend (POST)**: Spend points following the rules of spending the oldest points first without allowing any payer to go negative.
- **/balance (GET)**: View the user's current alance of points broken down by payer.


## Installation and Usage Instructions

### Step 0: Install Python

Make sure you have Python 3.8+ installed on your machine. If you don't have Python installed, you can follow the instructions from [python.org](https://www.python.org/downloads/).

### Step 1: Clone the project

First, clone this repository to your local machine:

```bash
git clone https://github.com/andrew-sha/fetch-coding-exercise.git
cd fetch-coding-exercise/
```

### Step 2: Install dependencies
Create a virtual environment using 

```bash
python3 -m venv .env
```

This will serve as a self-isolated environment in which the project's dependencies will be installed. Now activate the environment via

```bash
source .env/bin/activate
```

and finally install the required dependencies using 

```bash
pip install -r requirements.txt
```

### Step 3: Run and test service
To run the service, run

```bash
python3 points.py
```

This will begin serving the API on your local machine via port 8000. To interact with the API, use the `curl` utility from your command line. For example, to add 500 points from the payer Dannon to the user's account, run 

```bash
curl -X POST http://127.0.0.1:8000/add -H "Content-Type: application/json" -d '{"payer": "DANNON", "points": 5000, "timestamp": "2022-10-31T14:00:00Z"}'
```

Alternatively, to test the API on the test case provided in the specifications, run the following from within the project's virtual environment

```bash
python3 test_points.py
```
