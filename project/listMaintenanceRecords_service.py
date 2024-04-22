from datetime import datetime
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class GetMaintenanceRequest(BaseModel):
    """
    Request model for fetching maintenance logs. This model does not require any specific query or path parameters, as it retrieves all maintenance logs.
    """

    pass


class MaintenanceBrief(BaseModel):
    """
    A compact representation of maintenance details.
    """

    equipmentName: str
    maintenanceType: str
    maintenanceDate: datetime


class GetMaintenanceResponse(BaseModel):
    """
    Response model for a list of abbreviated maintenance details. Provides essential information for quick overview of maintenance schedules and histories.
    """

    maintenanceRecords: List[MaintenanceBrief]


async def listMaintenanceRecords(
    request: GetMaintenanceRequest,
) -> GetMaintenanceResponse:
    """
    Retrieves a list of all maintenance records. Each record will show brief details like machine name, maintenance type, and date. This helps in quickly viewing upcoming or past maintenances.

    Args:
        request (GetMaintenanceRequest): Request model for fetching maintenance logs. This model does not require any specific query or path parameters, as it retrieves all maintenance logs.

    Returns:
        GetMaintenanceResponse: Response model for a list of abbreviated maintenance details. Provides essential information for quick overview of maintenance schedules and histories.
    """
    maintenance_logs = await prisma.models.MaintenanceLog.prisma().find_many(
        include={"Equipment": True}
    )
    maintenance_records = [
        MaintenanceBrief(
            equipmentName=log.Equipment.name,
            maintenanceType=log.description,
            maintenanceDate=log.completionDate
            if log.completionDate
            else datetime.now(),
        )
        for log in maintenance_logs
    ]
    return GetMaintenanceResponse(maintenanceRecords=maintenance_records)
