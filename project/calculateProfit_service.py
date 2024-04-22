from typing import Dict, Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class ProfitCalculationResponse(BaseModel):
    """
    Response model that provides the calculated potential profits and additional statistics for better planning.
    """

    estimatedProfit: float
    additionalStats: Dict[str, float]


async def fetch_board_foot_price(
    treeType: prisma.enums.TreeType, diameter: float, height: float
) -> Optional[float]:
    """
    Fetches the price per board foot of wood based on the tree type, height, and diameter from the database.

    This function queries the `BoardFootCalculator` model in the database to find an entry matching the given
    tree type, diameter, and height. If a matching entry is found, it converts and returns the price per board foot.
    Otherwise, it returns None if no matching record is found.

    Args:
        treeType (prisma.enums.TreeType): The type of the tree.
        diameter (float): Diameter of the tree in inches.
        height (float): Height of the tree in feet.

    Returns:
        Optional[float]: Price per board foot if record exists, else None.

    Example:
        tree_type = prisma.enums.TreeType.OAK
        diameter = 12.0
        height = 20.0
        price = await fetch_board_foot_price(tree_type, diameter, height)
        >>> price  # Might print something like 2.50 if a record exists, or None if no such record
    """
    record = await prisma.models.BoardFootCalculator.prisma().find_first(
        where={"treeType": treeType, "diameter": diameter, "height": height}
    )
    return float(record.pricePerBoardFoot) if record else None


class BoardFootCalculator:
    pricePerBoardFoot: float


def calculate_board_feet(height: float, diameter: float) -> float:
    """
    Calculate the board feet of lumber yielded by a tree using the formula:
    board_feet = (diameter^2 * height) / 12

    Args:
        height (float): The height of the tree in feet.
        diameter (float): The diameter of the tree at breast height in inches.

    Returns:
        float: The calculated board feet.
    """
    return diameter**2 * height / 12


async def calculateProfit(
    treeType: prisma.enums.TreeType, height: float, diameter: float
) -> ProfitCalculationResponse:
    """
    This endpoint calculates the potential profit based on the provided tree parameters such as type, height, and diameter. It takes the inputs, applies the board foot calculation formula, and multiplies the result by the current market price per board foot. The endpoint ensures data is in a proper format and integrates with the Sales Module to provide required data. Expected to return profits estimation and potentially useful statistics for planning.

    Args:
    treeType (prisma.enums.TreeType): Type of the tree from which the wood is sourced; must be one of the defined prisma.enums.TreeType enums.
    height (float): Height of the tree in feet, which affects the volume of wood available.
    diameter (float): Diameter of the tree at breast height (in inches) affects the board foot calculations.

    Returns:
    ProfitCalculationResponse: Response model that provides the calculated potential profits and additional statistics for better planning.
    """
    board_feet = calculate_board_feet(height, diameter)
    price_per_board_foot = await fetch_board_foot_price(treeType, diameter, height)
    if price_per_board_foot is None:
        return ProfitCalculationResponse(
            estimatedProfit=0.0,
            additionalStats={
                "error": "No pricing available for the specified dimensions"
            },
        )
    estimated_profit = board_feet * price_per_board_foot
    return ProfitCalculationResponse(
        estimatedProfit=estimated_profit, additionalStats={"boardFeet": board_feet}
    )
