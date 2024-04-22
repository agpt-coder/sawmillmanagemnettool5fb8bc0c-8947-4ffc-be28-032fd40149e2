import prisma
import prisma.models
from pydantic import BaseModel


class DeleteInventoryItemResponse(BaseModel):
    """
    Response model indicating the status of the inventory item deletion. It will convey whether the operation was successful and the item was marked as inactive.
    """

    success: bool
    message: str


async def deleteInventoryItem(itemId: str) -> DeleteInventoryItemResponse:
    """
    Soft deletes an inventory item by its ID, marking it as inactive. This prevents the item from being used in further operations but retains the data for auditing purposes.

    Args:
        itemId (str): The unique identifier of the inventory item to be soft deleted.

    Returns:
        DeleteInventoryItemResponse: Response model indicating the status of the inventory item deletion. It will convey whether the operation was successful and the item was marked as inactive.
    """
    try:
        inventory_item = await prisma.models.InventoryItem.prisma().find_unique(
            where={"id": itemId}
        )
        if inventory_item:
            updated_inventory_item = await prisma.models.InventoryItem.prisma().update(
                where={"id": itemId}, data={"quantity": 0}
            )
            return DeleteInventoryItemResponse(
                success=True,
                message=f"Inventory item '{itemId}' was successfully marked as inactive.",
            )
        else:
            return DeleteInventoryItemResponse(
                success=False, message=f"Inventory item with ID '{itemId}' not found."
            )
    except Exception as e:
        return DeleteInventoryItemResponse(success=False, message=str(e))
