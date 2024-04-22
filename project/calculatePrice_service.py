from enum import Enum
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class CalculatePriceResponse(BaseModel):
    """
    Response model representing the calculated cost with potential factors impacting the final price.
    """

    totalPrice: float
    adjustments: List[str]


class ItemType(Enum):
    MATERIAL: str = "MATERIAL"
    PRODUCT: str = "PRODUCT"
    RESOURCE: str = "RESOURCE"


async def calculatePrice(
    itemType: ItemType, quantity: int, customerType: str
) -> CalculatePriceResponse:
    """
    Provides an estimated cost for a potential order based on current board foot prices and quantity rules. It interacts with both public and private board foot calculators.

    Args:
        itemType (ItemType): Type of item from the Inventory to calculate the price for.
        quantity (int): Quantity of the items.
        customerType (str): Type of the customer to consider any special pricing or discounts.

    Returns:
        CalculatePriceResponse: Response model representing the calculated cost with potential factors impacting the final price.
    """
    board_foot_calculators = await prisma.models.BoardFootCalculator.prisma().find_many(
        where={
            "treeType": itemType.name,
            "isPublic": False if customerType == "PRIVATE" else True,
        },
        order={"createdAt": "desc"},
        take=1,
    )
    if not board_foot_calculators:
        return CalculatePriceResponse(
            totalPrice=0.0,
            adjustments=["No price data available for selected item type."],
        )
    price_per_board_foot = float(board_foot_calculators[0].pricePerBoardFoot)
    total_price = price_per_board_foot * quantity
    adjustments = []
    discount_percentage = 0.05 if customerType == "VIP" and quantity > 10 else 0.0
    if discount_percentage > 0:
        discount_amount = total_price * discount_percentage
        total_price -= discount_amount
        adjustments.append(
            f"Applied {discount_percentage * 100}% discount for bulk purchase by a VIP customer."
        )
    return CalculatePriceResponse(totalPrice=total_price, adjustments=adjustments)
