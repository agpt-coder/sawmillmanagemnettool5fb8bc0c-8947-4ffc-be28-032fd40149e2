import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class InventoryItemResponse(BaseModel):
    """
    Response model representing the newly created inventory item, confirming the stored details.
    """

    id: str
    name: str
    quantity: int
    itemType: prisma.enums.ItemType


class ItemType:
    MATERIAL: str = "MATERIAL"
    PRODUCT: str = "PRODUCT"
    RESOURCE: str = "RESOURCE"


async def createInventoryItem(
    name: str, quantity: int, itemType: prisma.enums.ItemType
) -> InventoryItemResponse:
    """
    Allows creation of new inventory items. This route requires detailed information about the item, such as type, quantity, and status. Only accessible by admins to ensure proper management.

    Args:
        name (str): The name of the inventory item.
        quantity (int): The quantity of the inventory item available in stock.
        itemType (prisma.enums.ItemType): The type of the inventory item, which must be one of the predefined prisma.enums.ItemType enums.

    Returns:
        InventoryItemResponse: Response model representing the newly created inventory item, confirming the stored details.
    """
    new_item = await prisma.models.InventoryItem.prisma().create(
        data={"name": name, "quantity": quantity, "itemType": itemType}
    )
    return InventoryItemResponse(
        id=new_item.id,
        name=new_item.name,
        quantity=new_item.quantity,
        itemType=new_item.itemType,
    )
