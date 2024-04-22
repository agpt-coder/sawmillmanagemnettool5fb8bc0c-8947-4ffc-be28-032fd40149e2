from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class EmployeeDetails(BaseModel):
    """
    Sub-type that provides more detailed references to the assigned technician such as employee ID.
    """

    employeeId: str
    firstName: str
    lastName: str


class MaintenanceUpdateResponse(BaseModel):
    """
    Response model for the updated maintenance record. Returns the full updated record details.
    """

    success: bool
    updatedRecord: prisma.models.MaintenanceLog
    error: Optional[str] = None


async def updateMaintenanceRecord(
    recordId: str,
    maintenanceType: str,
    description: str,
    scheduledDate: Optional[datetime],
    technicianDetails: EmployeeDetails,
) -> MaintenanceUpdateResponse:
    """
    Updates an existing maintenance record. It can modify fields like maintenance type, date, and technician details. Ensures records are current and accurate.

    Args:
    recordId (str): The unique ID of the maintenance record to be updated.
    maintenanceType (str): The type of maintenance being performed.
    description (str): Description or details regarding the maintenance task.
    scheduledDate (Optional[datetime]): The scheduled date for the maintenance. Nullable if the date is to be removed or unspecified.
    technicianDetails (EmployeeDetails): Details of the technician assigned for the maintenance, including their employee ID.

    Returns:
    MaintenanceUpdateResponse: Response model for the updated maintenance record. Returns the full updated record details.
    """
    try:
        record = await prisma.models.MaintenanceLog.prisma().find_unique(
            where={"id": recordId}, include={"responsible": True}
        )
        if not record:
            return MaintenanceUpdateResponse(
                success=False, updatedRecord=None, error="Record not found"
            )
        updated_record = await prisma.models.MaintenanceLog.prisma().update(
            where={"id": recordId},
            data={
                "description": description,
                "completionDate": scheduledDate,
                "employeeId": technicianDetails.employeeId,
            },
            include={"responsible": True},
        )
        return MaintenanceUpdateResponse(success=True, updatedRecord=updated_record)
    except Exception as e:
        return MaintenanceUpdateResponse(
            success=False, updatedRecord=None, error=str(e)
        )
