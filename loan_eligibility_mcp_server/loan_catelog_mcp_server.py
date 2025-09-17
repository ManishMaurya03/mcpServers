import json
from mcp.server.fastmcp import FastMCP

app = FastMCP("loan-product-catalog-server")

# Mock loan product catalog
LOAN_PRODUCTS = [
    {
        "product_name": "Home Loan",
        "min_income": 50000,
        "min_credit_score": 700,
        "max_age": 60,
        "interest_rate": 8.2,
        "loan_amount_range": "5L - 50L"
    },
    {
        "product_name": "Car Loan",
        "min_income": 30000,
        "min_credit_score": 650,
        "max_age": 65,
        "interest_rate": 9.5,
        "loan_amount_range": "1L - 10L"
    },
    {
        "product_name": "Personal Loan",
        "min_income": 25000,
        "min_credit_score": 600,
        "max_age": 60,
        "interest_rate": 12.0,
        "loan_amount_range": "0.5L - 5L"
    },
    {
        "product_name": "Business Loan",
        "min_income": 75000,
        "min_credit_score": 750,
        "max_age": 65,
        "interest_rate": 10.5,
        "loan_amount_range": "10L - 100L"
    }
]

# Tool 1: Return all loan products
@app.tool()
def get_loan_products() -> str:
    """
    Returns all loan products with eligibility criteria.
    """
    return json.dumps(LOAN_PRODUCTS, indent=2)

# Tool 2: Return loan products filtered by min income
@app.tool()
def get_loan_products_by_income(income: float) -> str:
    """
    Returns loan products where customer's income >= product min_income
    """
    eligible_products = [
        product for product in LOAN_PRODUCTS if income >= product["min_income"]
    ]
    if not eligible_products:
        return f"No loan products available for income: {income}"
    return json.dumps(eligible_products, indent=2)

if __name__ == "__main__":
    app.run()