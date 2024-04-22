import prisma
import prisma.models
from pydantic import BaseModel


class DeleteScheduleResponse(BaseModel):
    """
    This response model confirms whether the schedule has been successfully deleted.
    """

    success: bool
    message: str


async def deleteSchedule(scheduleId: str) -> DeleteScheduleResponse:
    """
    Deletes a schedule by its ID. This is particularly necessary when plans
    change drastically or operations are ceased for a specific set of reasons,
    such as maintenance or downtime.

    Args:
        scheduleId (str): The unique identifier of the schedule to be deleted.

    Returns:
        DeleteScheduleResponse: This response model confirms whether the
        schedule has been successfully deleted.

    Example:
        scheduleId = 'schedule-uuid-1234'
        response = deleteSchedule(scheduleId)
        response.success  # True if deletion successful, False otherwise
        response.message  # Detailed message about the deletion
    """
    equipment = await prisma.models.Equipment.prisma().find_first(
        where={"maintenanceSchedule": scheduleId}, include={"MaintenanceLogs": True}
    )
    if not equipment:
        return DeleteScheduleResponse(success=False, message="Schedule not found.")
    await prisma.models.MaintenanceLog.prisma().delete_many(
        where={"equipmentId": equipment.id}
    )
    await prisma.models.Equipment.prisma().update(
        where={"id": equipment.id}, data={"maintenanceSchedule": None}
    )
    return DeleteScheduleResponse(
        success=True, message="Schedule deleted successfully."
    )
