from datetime import datetime
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class GetSchedulesRequest(BaseModel):
    """
    Request model for fetching all schedules. No specific request parameters required as it fetches all existing entries.
    """

    pass


class Shift(BaseModel):
    """
    Represents a work shift that includes timings and assigned equipment.
    """

    startTime: datetime
    endTime: datetime
    employeeId: str
    equipmentId: List[str]


class Schedule(BaseModel):
    """
    Detailed object containing information about a particular schedule, linking employees, shifts, and equipment.
    """

    employee: prisma.models.Employee
    shift: Shift
    equipment: prisma.models.Equipment
    start_time: datetime
    end_time: datetime


class GetSchedulesResponse(BaseModel):
    """
    Response model that contains an array of schedule data including details on employees, shifts, and equipment.
    """

    schedules: List[Schedule]


class Employee(BaseModel):
    """
    Detailed information about an employee.
    """

    id: str
    userId: str
    firstName: str
    lastName: str
    position: str


class Equipment(BaseModel):
    """
    Detailed information about equipment including its usage and maintenance schedules.
    """

    id: str
    name: str
    maintenanceSchedule: str


async def listSchedules(request: GetSchedulesRequest) -> GetSchedulesResponse:
    """
    Retrieves a list of all schedules. This endpoint can be used by the management team to overview operational planning
    and current engagement of resources and employees.

    Args:
        request (GetSchedulesRequest): Request model for fetching all schedules. No specific request parameters required
                                       as it fetches all existing entries.

    Returns:
        GetSchedulesResponse: Response model that contains an array of schedule data including details on employees,
                              shifts, and equipment.
    """
    shift_records = await prisma.models.Shift.prisma().find_many(
        include={"prisma.models.Employee": True}
    )
    schedules = []
    for shift_record in shift_records:
        equipment_records = await prisma.models.MaintenanceLog.prisma().find_many(
            where={"employeeId": shift_record.employeeId},
            include={"prisma.models.Equipment": True},
        )
        equipments = [
            prisma.models.Equipment(
                id=log.Equipment.id,
                name=log.Equipment.name,
                maintenanceSchedule=log.Equipment.maintenanceSchedule,
            )
            for log in equipment_records
        ]
        schedule = Schedule(
            employee=prisma.models.Employee(
                id=shift_record.Employee.id,
                userId=shift_record.Employee.userId,
                firstName=shift_record.Employee.firstName,
                lastName=shift_record.Employee.lastName,
                position=shift_record.Employee.position.name,
            ),
            shift=Shift(
                id=shift_record.id,
                startTime=shift_record.startTime,
                endTime=shift_record.endTime,
                employeeId=shift_record.employeeId,
            ),
            equipments=equipments,
        )  # TODO(autogpt): Argument missing for parameter "equipmentId". reportCallIssue
        schedules.append(schedule)
    return GetSchedulesResponse(schedules=schedules)
