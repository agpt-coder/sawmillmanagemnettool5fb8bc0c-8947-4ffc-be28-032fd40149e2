from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class OrderItem(BaseModel):
    """
    Represents an item in the order, including its database ID and the quantity ordered.
    """

    inventoryItemId: str
    quantity: int


class CreateOrderResponse(BaseModel):
    """
    Response model for the created order, providing the order ID after a successful transaction.
    """

    orderId: str


async def createOrder(customerId: str, items: List[OrderItem]) -> CreateOrderResponse:
    """
    Creates a new customer order. It uses inventory data to validate stock before confirming the order.
    Returns the order ID upon successful creation.

    The function first validates if all items in the order have sufficient stock in the inventory.
    If stock is sufficient, it reduces the inventory and creates a new order record in the SalesOrder table.

    Args:
        customerId (str): The unique identifier for the customer placing the order.
        items (List[OrderItem]): List of items with their quantities to be ordered.

    Returns:
        CreateOrderResponse: Response model for the created order, providing the order ID after a successful transaction.

    Raises:
        ValueError: If the inventory does not have enough stock for any item in the order.
    """
    for item in items:
        inventory_item = await prisma.models.InventoryItem.prisma().find_unique(
            where={"id": item.inventoryItemId}
        )
        if inventory_item is None or inventory_item.quantity < item.quantity:
            raise ValueError(f"Not enough stock for item ID {item.inventoryItemId}")
    for item in items:
        await prisma.models.InventoryItem.prisma().update(
            where={"id": item.inventoryItemId},
            data={"quantity": {"decrement": item.quantity}},
        )
    sales_order = await prisma.models.SalesOrder.prisma().create(
        data={"customerId": customerId, "status": "PENDING"}
    )
    return CreateOrderResponse(orderId=sales_order.id)
