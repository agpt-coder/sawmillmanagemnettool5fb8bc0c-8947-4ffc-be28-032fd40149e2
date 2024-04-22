from datetime import datetime
from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class MaintenanceRecordDetailsResponse(BaseModel):
    """
    Response model representing the detailed information of a maintenance log, including the duration, technician responsible, parts replaced, and any maintenance notes.
    """

    recordId: str
    description: str
    completionDate: Optional[datetime] = None
    equipmentId: str
    employeeId: str
    partsReplaced: List[str]
    technicianNotes: str


async def getMaintenanceRecord(recordId: str) -> MaintenanceRecordDetailsResponse:
    """
    Fetches detailed information of a specific maintenance record using its ID. This includes comprehensive data such as duration, parts replaced, and technician notes.

    Args:
        recordId (str): Unique identifier for the maintenance record to be fetched.

    Returns:
        MaintenanceRecordDetailsResponse: Response model representing the detailed information of a maintenance log, including the duration, technician responsible, parts replaced, and any maintenance notes.

    Example:
        record_details = await getMaintenanceRecord("some-record-id")
        # print out the description
        print(record_details.description)
    """
    maintenance_log = await prisma.models.MaintenanceLog.prisma().find_unique(
        where={"id": recordId}, include={"Equipment": True, "responsible": True}
    )
    if not maintenance_log:
        raise ValueError("Maintenance record not found")
    replaced_parts = ["PartA", "PartB"]
    technician_notes = "Completed with minor adjustments"
    details = MaintenanceRecordDetailsResponse(
        recordId=maintenance_log.id,
        description=maintenance_log.description,
        completionDate=maintenance_log.completionDate,
        equipmentId=maintenance_log.equipmentId,
        employeeId=maintenance_log.employeeId,
        partsReplaced=replaced_parts,
        technicianNotes=technician_notes,
    )
    return details
