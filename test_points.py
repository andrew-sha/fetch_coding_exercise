import requests
import json

BASE_URL = "http://localhost:8000"

def test_points_api():
    transactions = [
        {"payer": "DANNON", "points": 300, "timestamp": "2022-10-31T10:00:00Z"},
        {"payer": "UNILEVER", "points": 200, "timestamp": "2022-10-31T11:00:00Z"},
        {"payer": "DANNON", "points": -200, "timestamp": "2022-10-31T15:00:00Z"},
        {"payer": "MILLER COORS", "points": 10000, "timestamp": "2022-11-01T14:00:00Z"},
        {"payer": "DANNON", "points": 1000, "timestamp": "2022-11-02T14:00:00Z"}
    ]
    
    # call /add endpoint for each transaction
    for transaction in transactions:
        response = requests.post(f"{BASE_URL}/add", 
                                 data=json.dumps(transaction), 
                                 headers={'Content-Type': 'application/json'})
        assert response.status_code == 200

    # call /spend endpoint to spend 5000 points
    spend_request = {"points": 5000}
    response = requests.post(f"{BASE_URL}/spend", 
                             data=json.dumps(spend_request), 
                             headers={'Content-Type': 'application/json'})
    

    assert response.status_code == 200
    print(f"Spent 5000 points")
    
    # carse the response data
    spend_result = json.loads(response.text)
    
    # expected result
    expected_spend_result = [
        {"payer": "DANNON", "points": -300},
        {"payer": "UNILEVER", "points": -200},
        {"payer": "MILLER COORS", "points": -4700}
    ]

    assert spend_result == expected_spend_result
    print("Spend result matches expected output.")

    # call /balance endpoint to verify remaining balance after spend
    response = requests.get(f"{BASE_URL}/balance")

    # parse the response data
    balance_result = json.loads(response.text)

    # expected balance result
    expected_balance_result = {
        "DANNON": 1000,
        "UNILEVER" : 0,
        "MILLER COORS": 5300
    }

    assert balance_result == expected_balance_result
    print("Balance result matches expected output.")

if __name__ == "__main__":
    test_points_api()
