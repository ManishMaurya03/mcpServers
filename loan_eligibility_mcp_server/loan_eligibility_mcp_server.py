import json
from mcp.server.fastmcp import FastMCP
import requests

app = FastMCP("eligibility-engine-server")

# MCP server endpoints (for demo, assuming they are running locally)
CUSTOMER_PROFILE_URL = "http://localhost:8001"  # Replace with actual MCP endpoint if needed
CREDIT_BUREAU_URL = "http://localhost:8002"
LOAN_CATALOG_URL = "http://localhost:8003"

@app.tool()
def check_loan_eligibility(customer_id: str) -> str:
    """
    Checks loan eligibility based on:
      1. Customer profile
      2. Credit score
      3. Loan product rules
    """
    try:
        # 1️⃣ Fetch customer profile
        profile_resp = requests.post(f"{CUSTOMER_PROFILE_URL}/get_customer_profile", json={"customer_id": customer_id})
        customer = profile_resp.json() if profile_resp.ok else {}
        
        # 2️⃣ Fetch credit score
        credit_resp = requests.post(f"{CREDIT_BUREAU_URL}/get_credit_score", json={"customer_id": customer_id})
        credit_score = int(credit_resp.text.split()[-1]) if credit_resp.ok else 0
        
        # 3️⃣ Fetch loan products
        loan_resp = requests.get(f"{LOAN_CATALOG_URL}/get_loan_products")
        loan_products = loan_resp.json() if loan_resp.ok else []

        # 4️⃣ Determine eligibility
        eligible_loans = []
        not_eligible = []

        for product in loan_products:
            reason = ""
            if customer.get("income", 0) < product["min_income"]:
                reason = f"Income below {product['min_income']}"
            elif credit_score < product["min_credit_score"]:
                reason = f"Credit score below {product['min_credit_score']}"
            elif customer.get("age", 0) > product["max_age"]:
                reason = f"Age exceeds {product['max_age']}"
            
            if reason:
                not_eligible.append({"product": product["product_name"], "reason": reason})
            else:
                eligible_loans.append({
                    "product": product["product_name"],
                    "max_amount": product["loan_amount_range"],
                    "interest_rate": product["interest_rate"]
                })

        return json.dumps({
            "customer_id": customer_id,
            "eligible_loans": eligible_loans,
            "not_eligible": not_eligible
        }, indent=2)

    except Exception as e:
        return f"Error checking eligibility: {e}"

if __name__ == "__main__":
    app.run()