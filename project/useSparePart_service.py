from datetime import datetime
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class PartUsage(BaseModel):
    """
    Represents a spare part and the quantity used.
    """

    partId: str
    quantityUsed: int


class InventoryState(BaseModel):
    """
    Details the remaining quantity of a specific inventory item.
    """

    partId: str
    remainingQuantity: int


class MaintenancePartsLogResponse(BaseModel):
    """
    Response model that confirms the logging of spare parts and inventory adjustment.
    """

    success: bool
    updatedRecord: prisma.models.MaintenanceLog
    remainingInventory: List[InventoryState]


async def useSparePart(
    recordId: str, parts: List[PartUsage]
) -> MaintenancePartsLogResponse:
    """
    Logs the usage of spare parts for a specific maintenance record, updates inventory levels, and ensures
    accurate tracking of part usage.

    Args:
    recordId (str): The unique identifier of the maintenance record.
    parts (List[PartUsage]): List of parts and quantities used during the maintenance.

    Returns:
    MaintenancePartsLogResponse: Response model that confirms the logging of spare parts and inventory adjustment.

    Example:
        part_usage_list = [
            PartUsage(partId="part123", quantityUsed=2),
            PartUsage(partId="part456", quantityUsed=1)
        ]
        response = await useSparePart("record123", part_usage_list)
        print(response)
    """
    maintenance_record = await prisma.models.MaintenanceLog.prisma().find_unique(
        where={"id": recordId}
    )
    if not maintenance_record:
        return MaintenancePartsLogResponse(
            success=False, updatedRecord=None, remainingInventory=[]
        )
    remaining_inventory = []
    all_success = True
    for part in parts:
        inventory_item = await prisma.models.InventoryItem.prisma().find_unique(
            where={"id": part.partId}
        )
        if inventory_item and inventory_item.quantity >= part.quantityUsed:
            new_quantity = inventory_item.quantity - part.quantityUsed
            await prisma.models.InventoryItem.prisma().update(
                where={"id": part.partId}, data={"quantity": new_quantity}
            )
            remaining_inventory.append(
                InventoryState(partId=part.partId, remainingQuantity=new_quantity)
            )
            await prisma.models.InventoryLog.prisma().create(
                data={
                    "changeAmount": -part.quantityUsed,
                    "timestamp": datetime.now(),
                    "inventoryItemId": part.partId,
                }
            )
        else:
            all_success = False
    updated_maintenance_record = (
        await prisma.models.MaintenanceLog.prisma().find_unique(where={"id": recordId})
    )
    return MaintenancePartsLogResponse(
        success=all_success,
        updatedRecord=updated_maintenance_record,
        remainingInventory=remaining_inventory,
    )
