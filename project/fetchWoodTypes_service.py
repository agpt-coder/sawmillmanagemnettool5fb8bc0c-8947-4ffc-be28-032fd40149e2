from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class GetWoodTypesRequest(BaseModel):
    """
    Retrieve information for all available wood types used in board foot calculations. No input parameters are required for this endpoint as it serves the request to provide static data.
    """

    pass


class WoodType(BaseModel):
    """
    Describes individual wood types and their specific characteristics that impact board foot calculations.
    """

    name: prisma.enums.TreeType
    averageDensity: float
    color: str
    hardnessRating: int


class GetWoodTypesResponse(BaseModel):
    """
    Provides a descriptive list of all wood types available for board foot calculations, detailing each tree type and necessary characteristics for calculation like average density if needed.
    """

    woodTypes: List[WoodType]


async def fetchWoodTypes(request: GetWoodTypesRequest) -> GetWoodTypesResponse:
    """
    Retrieves a list of available wood types and their characteristics. This information supports the board foot calculation by providing essential data for accurate cost estimation.

    Args:
        request (GetWoodTypesRequest): Retrieve information for all available wood types used in board foot calculations. No input parameters are required for this endpoint as it serves the request to provide static data.

    Returns:
        GetWoodTypesResponse: Provides a descriptive list of all wood types available for board foot calculations, detailing each tree type and necessary characteristics for calculation like average density if needed.
    """
    board_foot_data = await prisma.models.BoardFootCalculator.prisma().find_many()
    wood_types = [
        WoodType(
            name=entry.treeType.name,
            averageDensity=0.5,
            color="Brown",
            hardnessRating=500,
        )
        for entry in board_foot_data
    ]
    response = GetWoodTypesResponse(woodTypes=wood_types)
    return response
