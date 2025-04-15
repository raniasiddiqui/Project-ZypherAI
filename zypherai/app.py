from flask import Flask, request, jsonify
import time
import random
import uuid
import redis
import json
import threading
from typing import Dict

app = Flask(__name__)

# This sets up Redis connection, which was reccomeded that I use in this assessment. 
redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

# Mock model prediction function
def mock_model_predict(input: str) -> Dict[str, str]:
    time.sleep(random.randint(10, 17))  # Simulate processing delay
    result = str(random.randint(1000, 20000))
    output = {"input": input, "result": result}
    return output

# Worker function for processing queue items
def process_queue():
    while True:
        # Pop item from the prediction queue
        queue_item = redis_client.blpop("prediction_queue", timeout=1)
        if queue_item:
            _, prediction_data = queue_item
            prediction_data = json.loads(prediction_data)
            prediction_id = prediction_data['prediction_id']
            input_text = prediction_data['input']
            
            # Update status to processing
            redis_client.set(f"status:{prediction_id}", "processing")
            
            # Run prediction
            output = mock_model_predict(input_text)
            
            # Store result and update status
            redis_client.set(f"result:{prediction_id}", json.dumps(output))
            redis_client.set(f"status:{prediction_id}", "completed")
        time.sleep(0.1)  # Small delay to prevent CPU overuse

# The above function runs continiously in the background, processing items in the queue. It pops requets from the reddis queue and processes them.
# It runs the prediction function and stores the result in Redis, updating the status accordingly.

# /predict endpoint with async support
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    async_mode = request.headers.get("Async-Mode", "false").lower() == "true"

    if not data or 'input' not in data:
        return jsonify({"error": "Invalid input"}), 400

    input_text = data['input']

    if async_mode:
        prediction_id = str(uuid.uuid4())
        
        # Add to Redis queue for processing
        prediction_data = {
            'prediction_id': prediction_id,
            'input': input_text
        }
        redis_client.set(f"status:{prediction_id}", "queued")
        redis_client.rpush("prediction_queue", json.dumps(prediction_data))

        return jsonify({
            "message": "Request received. Processing asynchronously.",
            "prediction_id": prediction_id
        }), 202
    else:
        # Synchronous mode
        prediction = mock_model_predict(input_text)
        return jsonify(prediction), 200

# The above function handles POST requests to the /predict endpoint. 
# It checks if the request is async or not. If it is async, it generates a unique prediction ID and adds the request to a Redis queue for processing. 
# If not, it processes the request synchronously and returns the result.

# GET endpoint to fetch prediction by ID
@app.route('/predict/<prediction_id>', methods=['GET'])
def get_prediction(prediction_id):
    # Check if prediction exists
    status = redis_client.get(f"status:{prediction_id}")
    if not status:
        return jsonify({"error": "Prediction ID not found."}), 404

    if status == "processing" or status == "queued":
        return jsonify({"error": "Prediction is still being processed."}), 400

    # Get result
    result = redis_client.get(f"result:{prediction_id}")
    if result:
        output = json.loads(result)
        return jsonify({
            "prediction_id": prediction_id,
            "output": output
        }), 200
    else:
        return jsonify({"error": "Result not found for the given prediction ID."}), 404
    
#Handles GET requests to fetch the prediction result by ID.
# It checks the status of the prediction and returns the result if available.
# If the prediction is still being processed, it returns an error message saying its being processed.
# If the prediction ID is not found, it returns an error message saying the ID is not found. 

if __name__ == '__main__':
    # Start the worker thread
    worker_thread = threading.Thread(target=process_queue, daemon=True)
    worker_thread.start()
    
    # Start the Flask app
    app.run(host='0.0.0.0', port=8080)

# The above code starts the Flask app and the worker thread for processing the queue.
# The worker thread runs in the background, continuously checking the Redis queue for new prediction requests and processing them.
# The Flask app handles incoming requests and provides endpoints for making predictions and fetching results. 