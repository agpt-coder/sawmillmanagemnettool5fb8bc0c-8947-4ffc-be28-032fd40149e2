from datetime import datetime
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class ShiftDetail(BaseModel):
    """
    A model encapsulating the essential details of a work shift for scheduling.
    """

    start_time: datetime
    end_time: datetime
    employee_id: str


class EquipmentUsage(BaseModel):
    """
    Details the usage of a specific piece of equipment in the schedule.
    """

    equipment_id: str
    start_time: datetime
    end_time: datetime


class FetchScheduleDetailsResponse(BaseModel):
    """
    A detailed response model that providing the complete operational outlook including shifts, employees involved and any related machinery usage, optimized for real-time updates.
    """

    operations: List[str]
    shifts: List[ShiftDetail]
    machineryDetails: List[EquipmentUsage]


async def getSchedule(scheduleId: str) -> FetchScheduleDetailsResponse:
    """
    Fetches specific schedule details by ID. It provides information on the particular
    operations, shifts assigned, and machinery used for that day. Useful for operational adjustments and real-time updates.

    Args:
        scheduleId (str): Unique identifier for the schedule to fetch specific details.

    Returns:
        FetchScheduleDetailsResponse: A detailed response model that providing the complete operational outlook
        including shifts, employees involved and any related machinery usage, optimized for real-time updates.
    """
    shifts = await prisma.models.Shift.prisma().find_many(
        where={"id": scheduleId}, include={"Employee": True}
    )
    maintenance_logs = await prisma.models.MaintenanceLog.prisma().find_many(
        where={"Equipment": {"maintenanceSchedule": scheduleId}},
        include={"Equipment": True},
    )
    shift_details = [
        ShiftDetail(
            start_time=shift.startTime,
            end_time=shift.endTime,
            employee_id=shift.employeeId,
        )
        for shift in shifts
    ]
    equipment_usage = [
        EquipmentUsage(
            equipment_id=log.Equipment.id,
            start_time=log.Equipment.MaintenanceLogs[0].completionDate,
            end_time=log.Equipment.MaintenanceLogs[-1].completionDate,
        )
        for log in maintenance_logs
        if log.Equipment
    ]
    operations = ["Operation details could involve more specific business logic"]
    return FetchScheduleDetailsResponse(
        operations=operations, shifts=shift_details, machineryDetails=equipment_usage
    )
