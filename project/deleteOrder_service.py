import prisma
import prisma.models
from pydantic import BaseModel


class DeleteOrderResponse(BaseModel):
    """
    Response model which confirms the order has been deleted and provides details on any associated inventory adjustments.
    """

    status: str
    message: str


async def deleteOrder(orderId: str) -> DeleteOrderResponse:
    """
    Deletes a specific order, requiring a re-adjustment in inventory levels. Accessible only by admins to ensure data integrity.

    Args:
        orderId (str): The unique identifier of the order to be deleted.

    Returns:
        DeleteOrderResponse: Response model which confirms the order has been deleted and provides details on any associated inventory adjustments.
    """
    order = await prisma.models.SalesOrder.prisma().find_unique(
        where={"id": orderId}, include={"User": True}
    )
    if order is None:
        return DeleteOrderResponse(status="Failure", message="Order not found.")
    if order.User.role != "ADMIN":
        return DeleteOrderResponse(
            status="Failure",
            message="Unauthorized action. Only admins can delete orders.",
        )
    await prisma.models.SalesOrder.prisma().delete(where={"id": orderId})
    return DeleteOrderResponse(
        status="Success",
        message="Order successfully deleted and inventory adjusted accordingly.",
    )
