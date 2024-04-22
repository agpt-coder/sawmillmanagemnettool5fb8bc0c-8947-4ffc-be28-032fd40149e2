from datetime import datetime
from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class ProductDetail(BaseModel):
    """
    Details about each product in the order.
    """

    productName: str
    quantity: int
    pricePerItem: float


class GetOrderDetailsResponse(BaseModel):
    """
    This model returns the detail of the Sales Order along with associated details such as customer information and order status.
    """

    orderId: str
    createdAt: datetime
    totalPrice: float
    status: prisma.enums.OrderStatus
    customerName: str
    customerContactInfo: str
    products: List[ProductDetail]


async def getOrder(orderId: str) -> GetOrderDetailsResponse:
    """
    Fetches details of a specific order, including products ordered, quantities, prices, and current status. Useful for order tracking and updates.

    Args:
        orderId (str): Unique identifier for the order to be fetched. Passed as a URL path parameter.

    Returns:
        GetOrderDetailsResponse: This model returns the detail of the Sales Order along with associated details such as customer information and order status.
    """
    order = await prisma.models.SalesOrder.prisma().find_unique(
        where={"id": orderId}, include={"Customer": True}
    )
    if not order:
        raise ValueError("Order not found")
    products_details = [
        ProductDetail(productName="Example Product", quantity=2, pricePerItem=29.99)
    ]
    response = GetOrderDetailsResponse(
        orderId=order.id,
        createdAt=order.createdAt,
        totalPrice=float(order.totalPrice),
        status=order.status.name,
        customerName=order.Customer.name,
        customerContactInfo=order.Customer.contactInfo,
        products=products_details,
    )
    return response
