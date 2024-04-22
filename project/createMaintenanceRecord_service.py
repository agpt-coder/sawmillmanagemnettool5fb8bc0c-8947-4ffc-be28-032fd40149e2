from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class MaintenanceRecordResponse(BaseModel):
    """
    This model represents a maintenance record that has been created and includes all of the details of the record.
    """

    id: str
    equipmentId: str
    description: str
    completionDate: Optional[datetime] = None
    responsibleId: str


async def createMaintenanceRecord(
    equipmentId: str,
    description: str,
    completionDate: Optional[datetime],
    responsibleId: str,
) -> MaintenanceRecordResponse:
    """
    Creates a new maintenance record. It accepts details like equipment ID, type of maintenance, and date. Upon successful creation, it returns the created maintenance record.

    Args:
        equipmentId (str): The unique identifier for the equipment that needs maintenance.
        description (str): Description of the maintenance type or activities involved.
        completionDate (Optional[datetime]): The scheduled date for the maintenance. This field can be null if the maintenance is being scheduled but the date is not yet finalized.
        responsibleId (str): The ID of the employee responsible for this maintenance task.

    Returns:
        MaintenanceRecordResponse: This model represents a maintenance record that has been created and includes all the details of the record.
    """
    maintenance_log = await prisma.models.MaintenanceLog.prisma().create(
        data={
            "description": description,
            "completionDate": completionDate,
            "equipmentId": equipmentId,
            "employeeId": responsibleId,
        }
    )
    return MaintenanceRecordResponse(
        id=maintenance_log.id,
        equipmentId=maintenance_log.equipmentId,
        description=maintenance_log.description,
        completionDate=maintenance_log.completionDate,
        responsibleId=maintenance_log.employeeId,
    )
