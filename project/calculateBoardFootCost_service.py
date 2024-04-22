import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class BoardFootCalculateResponse(BaseModel):
    """
    Response object that provides the cost estimation after calculating board foot volume and applying pricing models, crucial for sales module functionality.
    """

    estimatedCost: float
    boardFootVolume: float


def calculate_board_foot_volume(diameter: float, height: float) -> float:
    """
    Computes the volume of wood in board feet using a simplified formula.

    Args:
        diameter (float): The diameter of the tree in inches.
        height (float): The height of the tree in feet.

    Returns:
        float: The calculated volume of wood in board feet.
    """
    return diameter * diameter * height / 12.0


async def calculateBoardFootCost(
    diameter: float, treeType: prisma.enums.TreeType, height: float
) -> BoardFootCalculateResponse:
    """
    Calculates the cost based on the input parameters: tree diameter, type, and height. This endpoint uses
    mathematical formulas to determine the board foot volume, then applies pricing models according to wood type.
    The result provides a cost estimate crucial for the Sales Module's preliminary cost calculation features.

    Args:
        diameter (float): Diameter of the tree in inches. This measurement will be used to calculate the board foot volume.
        treeType (prisma.enums.TreeType): Type of the tree, which influences the price per board foot based on the specific characteristics of the wood.
        height (float): Height of the tree in feet. Used together with diameter to calculate the total board foot volume.

    Returns:
        BoardFootCalculateResponse: Response object that provides the cost estimation after calculating board foot volume and applying pricing models, crucial for sales module functionality.
    """
    board_foot_volume = calculate_board_foot_volume(diameter, height)
    calculator = await prisma.models.BoardFootCalculator.prisma().find_first(
        where={"treeType": treeType}
    )
    if not calculator:
        raise ValueError(
            "Pricing information for the specified tree type is not available."
        )
    estimated_cost = board_foot_volume * float(calculator.pricePerBoardFoot)
    return BoardFootCalculateResponse(
        estimatedCost=estimated_cost, boardFootVolume=board_foot_volume
    )
