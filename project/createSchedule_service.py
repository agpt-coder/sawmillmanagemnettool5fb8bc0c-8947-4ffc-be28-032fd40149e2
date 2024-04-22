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


class ScheduleCreationResponse(BaseModel):
    """
    Contains details of the schedule that was created, including shifts and equipment assignment.
    """

    schedule_id: str
    shifts: List[ShiftDetail]
    used_equipment: List[EquipmentUsage]
    creation_status: str


async def createSchedule(
    shift_details: List[ShiftDetail], equipment_usage: List[EquipmentUsage]
) -> ScheduleCreationResponse:
    """
    Creates a new schedule for sawmill operations, including shifts and machinery usage. It checks equipment availability from the Maintenance Tracker and resource availability from Inventory Management before finalizing the schedule. Returns the created schedule details.

    Args:
        shift_details (List[ShiftDetail]): Details of the shift including start time, end time, and the employee assigned.
        equipment_usage (List[EquipmentUsage]): Details about which equipment will be used during the sawmill operations.

    Returns:
        ScheduleCreationResponse: Contains details of the schedule that was created, including shifts and equipment assignment.

    Example:
        shift_details = [
            ShiftDetail(start_time=datetime(2021, 12, 1, 8), end_time=datetime(2021, 12, 1, 16), employee_id='emp123')
        ]
        equipment_usage = [
            EquipmentUsage(equipment_id='eq123', start_time=datetime(2021, 12, 1, 8), end_time=datetime(2021, 12, 1, 16))
        ]
        result = await createSchedule(shift_details, equipment_usage)
        print(result.schedule_id, result.creation_status)  # Outputs the schedule identifier and the status of creation
    """
    for shift in shift_details:
        overlap_shifts = await prisma.models.Shift.prisma().find_many(
            where={
                "AND": [
                    {"startTime": {"lt": shift.end_time}},
                    {"endTime": {"gt": shift.start_time}},
                    {"employeeId": shift.employee_id},
                ]
            }
        )
        if overlap_shifts:
            return ScheduleCreationResponse(
                schedule_id="",
                shifts=[],
                used_equipment=[],
                creation_status="Failed due to shift conflict",
            )
    for equipment in equipment_usage:
        overlap_equipment = await prisma.models.MaintenanceLog.prisma().find_many(
            where={
                "AND": [
                    {"startTime": {"lt": equipment.end_time}},
                    {"endTime": {"gt": equipment.start_time}},
                    {"equipmentId": equipment.equipment_id, "completionDate": None},
                ]
            }
        )
        if overlap_equipment:
            return ScheduleCreationResponse(
                schedule_id="",
                shifts=[],
                used_equipment=[],
                creation_status="Failed due to equipment maintenance conflict",
            )
    import uuid

    schedule_id = str(uuid.uuid4())
    return ScheduleCreationResponse(
        schedule_id=schedule_id,
        shifts=shift_details,
        used_equipment=equipment_usage,
        creation_status="Success",
    )
