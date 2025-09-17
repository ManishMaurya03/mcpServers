# Purpose: Provides customer’s financial & demographic details.
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("customer-profile-server")

# Mock database (in real-world -> DB or API)
CUSTOMERS = {
    "C123": {
        "name": "Ravi Kumar",
        "age": 32,
        "income": 75000,
        "employment_status": "Salaried",
        "existing_loans": ["Car Loan"],
        "loan_repayment_history": "Good"
    },
    "C124": {
        "name": "Anita Sharma",
        "age": 45,
        "income": 40000,
        "employment_status": "Self-Employed",
        "existing_loans": ["Personal Loan"],
        "loan_repayment_history": "Average"
    },
    "C125": {
        "name": "Amit Singh",
        "age": 28,
        "income": 95000,
        "employment_status": "Salaried",
        "existing_loans": [],
        "loan_repayment_history": "Excellent"
    }
}

@mcp.tool()
def get_customer_profile(customer_id: str) -> str:
    """
    Fetch customer profile by customer_id
    """
    if customer_id in CUSTOMERS:
        return json.dumps(CUSTOMERS[customer_id], indent=2)
    else:
        return f"Customer ID {customer_id} not found."

if __name__ == "__main__":
    mcp.run() 