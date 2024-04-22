from enum import Enum

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class InventoryItem(BaseModel):
    """
    Model representing an item in the inventory, including its identifier, name, quantity, and type.
    """

    id: str
    name: str
    quantity: int
    itemType: prisma.enums.ItemType


class UpdateInventoryItemResponse(BaseModel):
    """
    Response model for the inventory update operation. Provides feedback on the execution of the update, including the updated state of the item.
    """

    success: bool
    updatedItem: InventoryItem


class ItemType(Enum):
    MATERIAL: str = "MATERIAL"
    PRODUCT: str = "PRODUCT"
    RESOURCE: str = "RESOURCE"


async def updateInventoryItem(
    itemId: str, name: str, quantity: int, itemType: prisma.enums.ItemType
) -> UpdateInventoryItemResponse:
    """
    Updates existing inventory item data. This is crucial for keeping inventory data up-to-date, reflecting new quantities or material states. Access is restricted to roles that manage inventory.

    Args:
        itemId (str): The unique identifier of the inventory item to update. Specified in the URL path.
        name (str): The updated name of the inventory item, if necessary.
        quantity (int): The updated quantity of the inventory item. Must reflect the actual physical count post-adjustment.
        itemType (prisma.enums.ItemType): The updated type of the inventory item, allows classification into categories such as MATERIAL, PRODUCT, RESOURCE.

    Returns:
        UpdateInventoryItemResponse: Response model for the inventory update operation. Provides feedback on the execution of the update, including the updated state of the item.

    Example:
        response = updateInventoryItem("1234", "Lumber", 50, prisma.enums.ItemType.MATERIAL)
        if response.success:
            print(f"Updated Item: {response.updatedItem}")
        else:
            print("Update failed")
    """
    inventory_item = await prisma.models.InventoryItem.prisma().find_unique(
        where={"id": itemId}
    )
    if inventory_item:
        updated_inventory_item = await prisma.models.InventoryItem.prisma().update(
            where={"id": itemId},
            data={"name": name, "quantity": quantity, "itemType": itemType.name},
        )
        return UpdateInventoryItemResponse(
            success=True, updatedItem=InventoryItem(**updated_inventory_item.dict())
        )
    else:
        return UpdateInventoryItemResponse(success=False, updatedItem=None)
