from flask import Flask, request, jsonify
app = Flask(__name__)
# Define the distances from centers to L1
distances = {
    'C1': 10,
    'C2': 20,
    'C3': 15
}

# Define the cost per km
cost_per_km = 5

# Define the stock at each center
stock = {
    'C1': {'A': 10, 'B': 10, 'C': 10},
    'C2': {'D': 10, 'E': 10, 'F': 10},
    'C3': {'G': 10, 'H': 10, 'I': 10}
}

def calculate_cost(order):
    # Calculate the cost for each center that can fulfill the entire order
    costs = []
    for center, products in stock.items():
        can_fulfill = True
        for product, quantity in order.items():
            if product not in products or products[product] < quantity:
                can_fulfill = False
                break
        if can_fulfill:
            cost = distances[center] * cost_per_km
            costs.append(cost)
    # Return the minimum cost
    return min(costs) if costs else -1

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the Delivery Cost API. Use POST /calculate_delivery_cost with your order JSON to get the delivery cost.'})

@app.route('/calculate_delivery_cost', methods=['POST', 'GET'])
def calculate_delivery_cost():
    if request.method == 'GET':
        return jsonify({
            'message': 'Send a POST request with JSON body containing your order. Example: {"A": 1, "G": 1, "H": 1, "I": 3}'
        })
    order = request.json
    cost = calculate_cost(order)
    if cost == -1:
        return jsonify({'error': 'Order cannot be fulfilled'}), 400
    return jsonify({'cost': cost})

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'The requested URL was not found on the server.'}), 404

if __name__ == '__main__':
    app.run(debug=True)
