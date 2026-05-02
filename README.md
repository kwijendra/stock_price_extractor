# stock_price_extractor
This project provides a FastAPI-based service to fetch financial data using the Alpha Vantage API.

## Instructions to Deploy

### Clone the git repository and checkout the relevant branch
'git clone https://github.com/kwijendra/stock_price_extractor.git'

### Create a Virtual Environment
'python -m venv venv'

### Activate the Virtual Environment
'.\venv\Scripts\Activate'

### Install Dependencies
'pip install -r requirements.txt'

### Set Alpha Vantage API Key
'$env:ALPHA_VANTAGE_KEY="ADDB8BJMY15TTTQ6"'

## Instructions to Run the Server

### Start the FastAPI server
'uvicorn main:app --reload'

### Use curl to query the API
Ex: curl http://127.0.0.1:8000/symbols/MSFT/annual/2024