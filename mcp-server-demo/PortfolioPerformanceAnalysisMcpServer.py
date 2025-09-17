from mcp.server.fastmcp import FastMCP, Context
import random

# Create MCP server instance
mcp = FastMCP("portfolio-analysis-server")

# Mock portfolio (client holdings)
# In real implementation, this can be fetched from DB or API
portfolio_data = {
    "Client123": [
        {"symbol": "AAPL", "sector": "Technology", "quantity": 10, "buy_price": 150},
        {"symbol": "MSFT", "sector": "Technology", "quantity": 5, "buy_price": 280},
        {"symbol": "JPM", "sector": "Financials", "quantity": 8, "buy_price": 130},
        {"symbol": "BND", "sector": "Bonds", "quantity": 20, "buy_price": 80}
    ]
}

# Helper: Simulate real-time stock price
def get_live_price(symbol: str) -> float:
    base_prices = {"AAPL": 170, "MSFT": 310, "JPM": 140, "BND": 82}
    return base_prices.get(symbol, 100) + random.uniform(-2, 2)

# MCP tool: Analyze portfolio
@mcp.tool()
def analyze_portfolio(client_id: str) -> dict:
    if client_id not in portfolio_data:
        return {"error": f"Portfolio not found for {client_id}"}

    holdings = portfolio_data[client_id]
    total_value = 0
    total_cost = 0
    sector_allocation = {}

    results = []
    for h in holdings:
        live_price = get_live_price(h["symbol"])
        current_value = h["quantity"] * live_price
        invested = h["quantity"] * h["buy_price"]
        pnl = current_value - invested

        total_value += current_value
        total_cost += invested
        sector_allocation[h["sector"]] = sector_allocation.get(h["sector"], 0) + current_value

        results.append({
            "symbol": h["symbol"],
            "sector": h["sector"],
            "quantity": h["quantity"],
            "buy_price": h["buy_price"],
            "live_price": round(live_price, 2),
            "pnl": round(pnl, 2)
        })

    performance = round(((total_value - total_cost) / total_cost) * 100, 2)

    return {
        "client_id": client_id,
        "total_invested": round(total_cost, 2),
        "current_value": round(total_value, 2),
        "performance_percent": performance,
        "holdings": results,
        "sector_allocation": {
            sector: round((val / total_value) * 100, 2)
            for sector, val in sector_allocation.items()
        }
    }

if __name__ == "__main__":
    mcp.run()