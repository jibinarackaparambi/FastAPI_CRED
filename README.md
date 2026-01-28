# FastAPI_CRED
Shipment API with FastAPI
A simple FastAPI application that exposes shipment data through REST endpoints.
This project demonstrates basic API design with query parameters and path variables, along with error handling.

🚀 Features
- Retrieve shipment details by query parameter (/shipment?id=1001)
- Retrieve shipment details by path parameter (/shipment/1001)
- Returns shipment information including:
- content (description of goods)
- status (delivery status)
- weight (shipment weight)
- Handles invalid IDs with proper HTTP exceptions (404 Not Found)

📂 Project Structure
project/
 ├── app.py   # FastAPI app with shipment endpoints
 └── README.md # Documentation

🛠 Requirements
- Python 3.10+
- FastAPI
- Uvicorn (ASGI server)
Install dependencies:
pip install fastapi uvicorn



▶️ Running the App
Start the server with Uvicorn:
uvicorn app:app --reload

- The app will be available at: http://127.0.0.1:8000 (127.0.0.1 in Bing)
- Interactive API docs: http://127.0.0.1:8000/docs (127.0.0.1 in Bing)
- Alternative docs (ReDoc): http://127.0.0.1:8000/redoc (127.0.0.1 in Bing)

📑 Endpoints
1. Get shipment by query parameter
Request:
GET /shipment?id=1001
Response:
{
  "content": "Electronics - Mobile Phones",
  "status": "In Transit",
  "weight": "12kg"
}

2. Get shipment by path parameter
Request:
GET /shipment/1002
Response:
{
  "content": "Books - Educational",
  "status": "Delivered",
  "weight": "8kg"
}
3. Error handling
If the shipment ID is missing or invalid:
{
  "detail": "Item not found"
}
4. POST shipment details
Request:
POST /shipment
Request:
{
    "id": 1007,
    "content": "Books - Noval",
    "status": "Delivered",
    "weight": "3kg"
}
Response:
{
    "id": 1007
}
5. PUT replace shipment details
Request:
PUT /shipment/1001?content=Jibin&status=Cancel&weight=45
Response:
{"content":"Jibin","status":"Cancel","weight":"45"}
6. PATCH update shipment details
Request:
PATCH /shipment/1001?status=Placed
Response:
{
    "content": "Electronics - Mobile Phones",
    "status": "Placed",
    "weight": "12kg"
}