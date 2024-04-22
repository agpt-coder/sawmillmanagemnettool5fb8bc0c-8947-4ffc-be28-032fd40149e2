import prisma
import prisma.models
from pydantic import BaseModel


class DeleteMaintenanceRecordResponse(BaseModel):
    """
    Response model that conveys the result of the DELETE operation on a maintenance record, confirming it was successfully deleted or if there was an error.
    """

    success: bool
    message: str


async def deleteMaintenanceRecord(recordId: str) -> DeleteMaintenanceRecordResponse:
    """
    Removes a maintenance record from the system. This is typically used when a record was created in error or the scheduled maintenance was cancelled.

    Args:
    recordId (str): The unique identifier of the maintenance record to be deleted. This value is provided as a path parameter.

    Returns:
    DeleteMaintenanceRecordResponse: Response model that conveys the result of the DELETE operation on a maintenance record, confirming it was successfully deleted or if there was an error.
    """
    maintenance_log = await prisma.models.MaintenanceLog.prisma().find_unique(
        where={"id": recordId}
    )
    if not maintenance_log:
        return DeleteMaintenanceRecordResponse(
            success=False, message="Maintenance record not found"
        )
    delete_result = await prisma.models.MaintenanceLog.prisma().delete(
        where={"id": recordId}
    )
    if delete_result:
        return DeleteMaintenanceRecordResponse(
            success=True, message="Maintenance record deleted successfully"
        )
    else:
        return DeleteMaintenanceRecordResponse(
            success=False, message="Failed to delete maintenance record"
        )
