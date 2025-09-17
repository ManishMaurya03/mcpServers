import random
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("credit-bureau-server")

# Mock credit scores (in real use case, fetch from Experian/Equifax API)
CUSTOMER_CREDIT_SCORE = {
    "C123": 735,
    "C124": 680,
    "C125": 790
}

@mcp.tool()
def get_credit_score(customer_id: str) -> str:
    """
    Fetch customer credit score by customer_id.
    If customer ID not found, generate a random score for demo purposes.
    """
    score = CUSTOMER_CREDIT_SCORE.get(customer_id, random.randint(650, 800))
    return f"Customer {customer_id} has a credit score of {score}."

if __name__ == "__main__":
    mcp.run()