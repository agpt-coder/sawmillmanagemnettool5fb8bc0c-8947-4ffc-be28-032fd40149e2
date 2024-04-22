from datetime import datetime
from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class InventoryLogDetails(BaseModel):
    """
    Detailed aspects of an individual inventory log entry associated with the inventory item.
    """

    logId: str
    timestamp: datetime
    changeAmount: int


class InventoryItemFetchResponse(BaseModel):
    """
    Response model containing detailed information about an inventory item, including type, quantity, and details about related inventory logs.
    """

    id: str
    name: str
    quantity: int
    itemType: prisma.enums.ItemType
    logs: List[InventoryLogDetails]


async def getInventoryItem(itemId: str) -> InventoryItemFetchResponse:
    """
    Fetches detailed information for a specific inventory item using the item's unique identifier. Information includes type, quantity, and resource details, useful for sales details and maintenance planning.

    Args:
    itemId (str): The unique identifier of the inventory item.

    Returns:
    InventoryItemFetchResponse: Response model containing detailed information about an inventory item, including type, quantity, and details about related inventory logs.
    """
    item = await prisma.models.InventoryItem.prisma().find_unique(
        where={"id": itemId}, include={"Logs": True}
    )
    if not item:
        raise ValueError("Item not found")
    logs = [
        InventoryLogDetails(
            logId=log.id, timestamp=log.timestamp, changeAmount=log.changeAmount
        )
        for log in item.Logs
    ]
    response = InventoryItemFetchResponse(
        id=item.id,
        name=item.name,
        quantity=item.quantity,
        itemType=item.itemType,
        logs=logs,
    )
    return response
