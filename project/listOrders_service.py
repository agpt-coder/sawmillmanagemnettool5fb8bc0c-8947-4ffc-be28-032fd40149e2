from datetime import datetime
from enum import Enum
from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class GetOrdersRequest(BaseModel):
    """
    Fetches all customer orders. No specific request parameters are needed hence we are utilizing an empty fields list for this model.
    """

    pass


class DetailedOrder(BaseModel):
    """
    Aggregates order and customer data for a complete view.
    """

    orderId: str
    customerName: str
    totalPrice: float
    orderStatus: prisma.enums.OrderStatus
    createdAt: datetime


class OrdersListResponse(BaseModel):
    """
    Provides a list of customer orders, each including customer details and order specifics.
    """

    orders: List[DetailedOrder]


class OrderStatus(Enum):
    PENDING: str = "Pending"
    COMPLETED: str = "Completed"
    CANCELLED: str = "Cancelled"


async def listOrders(request: GetOrdersRequest) -> OrdersListResponse:
    """
    Retrieves a list of all customer orders, including order details like customer name, order status, and total cost.

    Args:
    request (GetOrdersRequest): Fetches all customer orders. No specific request parameters are needed hence we are utilizing an empty fields list for this model.

    Returns:
    OrdersListResponse: Provides a list of customer orders, each including customer details and order specifics.
    """
    sales_orders = await prisma.models.SalesOrder.prisma().find_many(
        include={"Customer": True}
    )
    detailed_orders = [
        DetailedOrder(
            orderId=order.id,
            customerName=order.Customer.name,
            totalPrice=float(order.totalPrice),
            orderStatus=prisma.enums.OrderStatus(order.status),
            createdAt=order.createdAt,
        )
        for order in sales_orders
    ]
    return OrdersListResponse(orders=detailed_orders)
