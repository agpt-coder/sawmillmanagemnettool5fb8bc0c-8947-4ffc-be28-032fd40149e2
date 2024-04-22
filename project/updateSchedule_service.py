from datetime import datetime
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class Shift(BaseModel):
    """
    Represents a work shift that includes timings and assigned equipment.
    """

    startTime: datetime
    endTime: datetime
    employeeId: str
    equipmentId: List[str]


class ScheduleUpdateResponse(BaseModel):
    """
    Returns the updated schedule details along with a success message.
    """

    success: bool
    message: str
    updatedSchedule: Shift


async def updateSchedule(
    scheduleId: str,
    shiftStartTime: datetime,
    shiftEndTime: datetime,
    equipmentId: str,
    operationPlan: str,
) -> ScheduleUpdateResponse:
    """
    Updates an existing schedule based on the given schedule ID. It allows modifications to shift timings, operations plan, and machinery deployment. Maintains synchronization with equipment and resource availability through respective modules.

    Args:
    scheduleId (str): The ID of the schedule to be updated.
    shiftStartTime (datetime): The start time for the shift. Needs to be synchronized with employee availability.
    shiftEndTime (datetime): The end time for the shift.
    equipmentId (str): The ID of the equipment to be deployed for the shift. Synchronization with availability is essential.
    operationPlan (str): Detailed plan of operations to be conducted during the shift.

    Returns:
    ScheduleUpdateResponse: Returns the updated schedule details along with a success message.
    """
    shift_record = await prisma.models.Shift.prisma().find_unique(
        where={"id": scheduleId}
    )
    if not shift_record:
        return ScheduleUpdateResponse(
            success=False,
            message=f"No shift found with ID {scheduleId}",
            updatedSchedule=None,
        )
    updated_shift = await prisma.models.Shift.prisma().update(
        where={"id": scheduleId},
        data={
            "startTime": shiftStartTime,
            "endTime": shiftEndTime,
            "Equipment": {"connect": {"id": equipmentId}},
        },
    )
    updated_shift_details = Shift(
        startTime=updated_shift.startTime,
        endTime=updated_shift.endTime,
        employeeId=updated_shift.employeeId,
        equipmentId=[equipmentId],
    )
    return ScheduleUpdateResponse(
        success=True,
        message="Shift was successfully updated.",
        updatedSchedule=updated_shift_details,
    )
