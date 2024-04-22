from typing import Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class UpdateOrderResponse(BaseModel):
    """
    This model defines the structure of the response sent back by the server after updating an order. It includes the updated order details.
    """

    orderId: str
    quantity: int
    status: prisma.enums.OrderStatus
    updateSuccessful: bool
    message: Optional[str] = None


async def updateOrder(
    orderId: str, quantity: Optional[int], status: Optional[prisma.enums.OrderStatus]
) -> UpdateOrderResponse:
    """
    Updates an existing order's details, such as changes in quantity, product or cancellation of the order. Requires checks against inventory for stock adjustments.

    Args:
        orderId (str): The unique identifier of the order to be updated.
        quantity (Optional[int]): The new quantity of the product ordered. Must be checked against inventory.
        status (Optional[prisma.enums.OrderStatus]): The new status of the order which could be 'PENDING', 'COMPLETED', or 'CANCELLED'.

    Returns:
        UpdateOrderResponse: This model defines the structure of the response sent back by the server after updating an order.
        It includes the updated order details.
    """
    order = await prisma.models.SalesOrder.prisma().find_unique(where={"id": orderId})
    if not order:
        return UpdateOrderResponse(
            orderId=orderId,
            quantity=0,
            status=prisma.enums.OrderStatus.PENDING,
            updateSuccessful=False,
            message="Order not found.",
        )
    update_data = {}
    if quantity is not None and quantity != order.totalPrice:
        update_data["totalPrice"] = quantity
    if status is not None and status != order.status:
        update_data["status"] = status
    if update_data:
        order = await prisma.models.SalesOrder.prisma().update(
            where={"id": orderId}, data=update_data
        )
    return UpdateOrderResponse(
        orderId=orderId,
        quantity=quantity,
        status=status if status is not None else order.status,
        updateSuccessful=True,
        message="Order updated successfully.",
    )
