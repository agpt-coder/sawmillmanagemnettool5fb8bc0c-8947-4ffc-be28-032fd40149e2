from datetime import datetime

import httpx
from pydantic import BaseModel


class GetMarketPriceRequest(BaseModel):
    """
    Request model to fetch the latest market price for board foot calculations which involves no sendable data since it's a GET request. Access is restricted to certain user roles.
    """

    pass


class MarketPriceResponse(BaseModel):
    """
    Response model containing the latest market prices for board foot calculations. It provides the price and the timestamp of the last update to ensure the data's accuracy and timeliness.
    """

    market_price: float
    last_update: datetime


async def getCurrentMarketPrice(request: GetMarketPriceRequest) -> MarketPriceResponse:
    """
    Retrieves the current market price per board foot from an external financial service or a stored value updated periodically. This endpoint helps in keeping the profit calculations up-to-date with market fluctuations. Response should include the latest market price along with the time of the last update.

    Args:
        request (GetMarketPriceRequest): Request model to fetch the latest market price for board foot calculations which involves no sendable data since it's a GET request. Access is restricted to certain user roles.

    Returns:
        MarketPriceResponse: Response model containing the latest market prices for board foot calculations. It provides the price and the timestamp of the last update to ensure the data's accuracy and timeliness.

    Example:
        request = GetMarketPriceRequest()
        response = await getCurrentMarketPrice(request)
        print(response.market_price, response.last_update)
    """
    url = "https://api.example.com/marketprice/boardfoot"
    market_price: float = 0.0
    last_update: datetime = datetime.now()
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            market_price = float(data["market_price"])
            last_update = datetime.fromisoformat(data["last_update"])
    except Exception as e:
        print(f"Failed to get the market prices: {e}")
    return MarketPriceResponse(market_price=market_price, last_update=last_update)
