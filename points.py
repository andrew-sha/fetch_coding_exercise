from collections import defaultdict
from datetime import datetime
from flask import Flask, request, jsonify
from heapq import heappush, heappop


app = Flask(__name__)

transactions = []
payer_balances = defaultdict(int)
total_points = 0

@app.route('/add', methods=['POST'])
def add_points():
    global total_points
    # parse input
    data = request.json
    payer = data['payer']
    points = data['points']
    timestamp = datetime.strptime(data['timestamp'], "%Y-%m-%dT%H:%M:%SZ")
    
    # update total balance and individual payer balance
    payer_balances[payer] += points
    total_points += points
    
    # push transaction in the form (timestamp, (payer, points)) to min heap
    heappush(transactions, (timestamp, (payer, points)))
    
    return '', 200


@app.route('/spend', methods=['POST'])
def spend_points():
    global total_points
    # parse input
    data = request.json
    points_to_spend = data['points']
    
    if points_to_spend > total_points:
        return "Insufficient points", 400
        
    spent_points = []

    # spend available points, starting from oldest acquired points
    while points_to_spend:
        transaction = heappop(transactions)
        payer = transaction[1][0]
        points = transaction[1][1]
        points_spent = min(points_to_spend, points)

        points_to_spend -= points_spent
        payer_balances[payer] -= points_spent
        total_points -= points_spent

        # log expenditure if points were actually spent
        if points_spent > 0:
            spent_points.append({
                "payer": payer,
                "points": -points_spent
            })

        # re-log current transaction if not all points were spent
        if points_spent < points:
            heappush(transactions, (transaction[0], (payer, points - points_spent)))
    
    return jsonify(spent_points), 200


@app.route('/balance', methods=['GET'])
def get_balance():
    return jsonify(payer_balances), 200

if __name__ == '__main__':
    app.run(debug=True, port=8000)
