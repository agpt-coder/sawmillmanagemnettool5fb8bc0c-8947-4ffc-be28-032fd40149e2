from datetime import datetime
from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class GetCalculatorHistoryRequest(BaseModel):
    """
    Request model for fetching the historical records from the Board Foot Calculator. No specific fields are needed for this request as it primarily functions through GET retrieval.
    """

    pass


class CalculationRecord(BaseModel):
    """
    Details a single record of board foot calculation including all input parameters, the result, and timestamp data.
    """

    diameter: float
    treeType: prisma.enums.TreeType
    height: float
    pricePerBoardFoot: float
    calculatedProfit: float
    calculationTimestamp: datetime
    isPublic: bool


class GetCalculatorHistoryResponse(BaseModel):
    """
    A response model containing a list of all the historical calculations performed with the Board Foot Calculator. Each entry includes parameters used, result produced, and timestamps to help in analysis and auditing.
    """

    history: List[CalculationRecord]


async def viewCalculationHistory(
    request: GetCalculatorHistoryRequest,
) -> GetCalculatorHistoryResponse:
    """
    Provides a record of all previous profit calculations performed through the Board Foot Calculator. Each record should detail the inputs used and the output generated, along with timestamps. This helps in auditing and understanding past operational efficiencies.

    Args:
        request (GetCalculatorHistoryRequest): Request model for fetching the historical records from the Board Foot Calculator. No specific fields are needed for this request as it primarily functions through GET retrieval.

    Returns:
        GetCalculatorHistoryResponse: A response model containing a list of all the historical calculations performed with the Board Foot Calculator. Each entry includes parameters used, result produced, and timestamps to help in analysis and auditing.
    """
    records = await prisma.models.BoardFootCalculator.prisma().find_many()
    history = [
        CalculationRecord(
            diameter=r.diameter,
            treeType=r.treeType.name,
            height=r.height,
            pricePerBoardFoot=float(r.pricePerBoardFoot),
            calculatedProfit=r.diameter * r.height * float(r.pricePerBoardFoot),
            calculationTimestamp=datetime.now(),
            isPublic=r.isPublic,
        )
        for r in records
    ]
    return GetCalculatorHistoryResponse(history=history)
