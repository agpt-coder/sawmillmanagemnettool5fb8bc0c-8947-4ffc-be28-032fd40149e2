from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class GetInventoryRequest(BaseModel):
    """
    Request model for fetching inventory items. There are no input parameters as the endpoint fetches all inventory items.
    """

    pass


class InventoryItemDetailed(BaseModel):
    """
    Detailed information about each inventory item.
    """

    id: str
    name: str
    quantity: int
    itemType: prisma.enums.ItemType


class GetInventoryResponse(BaseModel):
    """
    Provides a list of all inventory items with detailed information. Useful for inventory checks and order processing by Admin and Salesperson roles.
    """

    inventory_items: List[InventoryItemDetailed]


async def listInventoryItems(request: GetInventoryRequest) -> GetInventoryResponse:
    """
    Retrieves a list of all inventory items including materials, products, and resources. This endpoint will be accessible to the admin and salesperson roles for order processing and inventory checks.

    Args:
        request (GetInventoryRequest): Request model for fetching inventory items. There are no input parameters as the endpoint fetches all inventory items.

    Returns:
        GetInventoryResponse: Provides a list of all inventory items with detailed information. Useful for inventory checks and order processing by Admin and Salesperson roles.
    """
    inventory_items = await prisma.models.InventoryItem.prisma().find_many()
    detailed_items = [
        InventoryItemDetailed(
            id=item.id,
            name=item.name,
            quantity=item.quantity,
            itemType=item.itemType.name,
        )
        for item in inventory_items
    ]
    response = GetInventoryResponse(inventory_items=detailed_items)
    return response
