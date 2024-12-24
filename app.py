from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class Customer(BaseModel):
    name: str
    email: str
    phone: str

class Transaction(BaseModel):
    customer_id: int
    transaction_date: datetime
    amount: float
    status: str

class RefundRequest(BaseModel):
    transaction_id: int
    customer_id: int
    refund_reason: str
    refund_status: Optional[str] = "Pending"

# @app.post("/customers/")
# def add_customer(customer: Customer):
#     # Insert customer data into Supabase
#     response = supabase.table("isbank_cutomers").insert(customer.dict()).execute()
#     if response:
#         return {"customer": response.data}
#     raise HTTPException(status_code=500, detail="Failed to add customer to database")

# @app.get("/customers/")
# def get_customers():
#     # Retrieve all customers from Supabase
#     response = supabase.table("isbank_cutomers").select("*").execute()
#     if response:
#         return response
#     raise HTTPException(status_code=500, detail="Failed to fetch customers from database")


# @app.get("/customers/{customer_id}", response_model=Optional[Customer])
# def get_customer(customer_id: int):
#     # Retrieve a specific customer by ID
#     response = supabase.table("isbank_cutomers").select("*").eq("id", customer_id).execute()
#     if response.data:
#         return response.data[0]
#     raise HTTPException(status_code=404, detail="Customer not found")

# @app.post("/transactions/")
# def add_transaction(transaction: Transaction):
#     # Convert datetime to ISO 8601 format for JSON compatibility
#     transaction_data = transaction.dict()
#     transaction_data['transaction_date'] = transaction.transaction_date.isoformat()
#
#     # Insert transaction into Supabase
#     response = supabase.table("isbank_transactions").insert(transaction_data).execute()
#     if response:
#         return {"message": "Transaction added successfully", "transaction": transaction_data}
#     raise HTTPException(status_code=500, detail="Failed to add transaction to database")

# @app.get("/transactions/", response_model=List[Transaction])
# def get_transactions():
#     # Retrieve all transactions from Supabase
#     response = supabase.table("isbank_transactions").select("*").execute()
#     if response:
#         return [
#             {
#                 **t,
#                 "transaction_date": datetime.fromisoformat(t["transaction_date"])  # Convert back to datetime
#             } for t in response.data
#         ]
#     raise HTTPException(status_code=500, detail="Failed to fetch transactions from database")


@app.get("/transactions/{transaction_id}", response_model=Transaction)
def get_transaction(transaction_id: int):
    # Retrieve a specific transaction by ID
    response = supabase.table("isbank_transactions").select("*").eq("id", transaction_id).execute()
    if response.data:
        transaction = response.data[0]
        transaction["transaction_date"] = datetime.fromisoformat(transaction["transaction_date"])
        return transaction
    raise HTTPException(status_code=404, detail="Transaction not found")

from typing import List

@app.get("/transactions/{customer_id}/transactions", response_model=List[Transaction])
def get_transactions(customer_id: int):
    # Retrieve all transactions for a specific customer ID
    response = supabase.table("isbank_transactions").select("*").eq("customer_id", customer_id).execute()
    if response.data:
        return response.data
    raise HTTPException(status_code=404, detail="No transactions found for the given customer ID")


@app.post("/refunds/")
def create_refund_request(refund_request: RefundRequest):
    response = supabase.table("isbank_refund").insert(refund_request.dict()).execute()
    if response:
        return {"refund": response.data[0]}
    raise HTTPException(status_code=500, detail="Failed to add customer to database")


@app.get("/refunds/{refund_id}", response_model=RefundRequest)
def get_refund_request(refund_id: int):
    response = supabase.table("isbank_refund").select("*").eq("id", refund_id).execute()
    if response.data:
        return response.data[0]
    raise HTTPException(status_code=404, detail="Refund request not found")
