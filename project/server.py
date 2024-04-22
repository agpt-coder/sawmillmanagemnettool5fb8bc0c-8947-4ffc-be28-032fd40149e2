import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List, Optional

import prisma
import prisma.enums
import project.calculateBoardFootCost_service
import project.calculatePrice_service
import project.calculateProfit_service
import project.createInventoryItem_service
import project.createMaintenanceRecord_service
import project.createOrder_service
import project.createSchedule_service
import project.deleteInventoryItem_service
import project.deleteMaintenanceRecord_service
import project.deleteOrder_service
import project.deleteSchedule_service
import project.fetchWoodTypes_service
import project.getCurrentMarketPrice_service
import project.getInventoryItem_service
import project.getMaintenanceRecord_service
import project.getOrder_service
import project.getSchedule_service
import project.listInventoryItems_service
import project.listMaintenanceRecords_service
import project.listOrders_service
import project.listSchedules_service
import project.updateInventoryItem_service
import project.updateMaintenanceRecord_service
import project.updateOrder_service
import project.updateSchedule_service
import project.useSparePart_service
import project.viewCalculationHistory_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="SawmillManagemnetTool",
    lifespan=lifespan,
    description="I run a simple backyard sawmill. I need software to manage and optimimze it",
)


@app.delete(
    "/schedules/{scheduleId}",
    response_model=project.deleteSchedule_service.DeleteScheduleResponse,
)
async def api_delete_deleteSchedule(
    scheduleId: str,
) -> project.deleteSchedule_service.DeleteScheduleResponse | Response:
    """
    Deletes a schedule by its ID. This is particularly necessary when plans change drastically or operations are ceased for a specific set of reasons, such as maintenance or downtime.
    """
    try:
        res = await project.deleteSchedule_service.deleteSchedule(scheduleId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/maintenance/{recordId}",
    response_model=project.deleteMaintenanceRecord_service.DeleteMaintenanceRecordResponse,
)
async def api_delete_deleteMaintenanceRecord(
    recordId: str,
) -> project.deleteMaintenanceRecord_service.DeleteMaintenanceRecordResponse | Response:
    """
    Removes a maintenance record from the system. This is typically used when a record was created in error or the scheduled maintenance was cancelled.
    """
    try:
        res = await project.deleteMaintenanceRecord_service.deleteMaintenanceRecord(
            recordId
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/maintenance",
    response_model=project.createMaintenanceRecord_service.MaintenanceRecordResponse,
)
async def api_post_createMaintenanceRecord(
    equipmentId: str,
    description: str,
    completionDate: Optional[datetime],
    responsibleId: str,
) -> project.createMaintenanceRecord_service.MaintenanceRecordResponse | Response:
    """
    Creates a new maintenance record. It accepts details like machine ID, type of maintenance, and date. Upon successful creation, it returns the created maintenance record.
    """
    try:
        res = await project.createMaintenanceRecord_service.createMaintenanceRecord(
            equipmentId, description, completionDate, responsibleId
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/maintenance/{recordId}",
    response_model=project.getMaintenanceRecord_service.MaintenanceRecordDetailsResponse,
)
async def api_get_getMaintenanceRecord(
    recordId: str,
) -> project.getMaintenanceRecord_service.MaintenanceRecordDetailsResponse | Response:
    """
    Fetches detailed information of a specific maintenance record using its ID. This includes comprehensive data such as duration, parts replaced, and technician notes.
    """
    try:
        res = await project.getMaintenanceRecord_service.getMaintenanceRecord(recordId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/inventory/{itemId}",
    response_model=project.deleteInventoryItem_service.DeleteInventoryItemResponse,
)
async def api_delete_deleteInventoryItem(
    itemId: str,
) -> project.deleteInventoryItem_service.DeleteInventoryItemResponse | Response:
    """
    Soft deletes an inventory item by its ID, marking it as inactive. This prevents the item from being used in further operations but retains the data for auditing purposes.
    """
    try:
        res = await project.deleteInventoryItem_service.deleteInventoryItem(itemId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/calculator/market-price",
    response_model=project.getCurrentMarketPrice_service.MarketPriceResponse,
)
async def api_get_getCurrentMarketPrice(
    request: project.getCurrentMarketPrice_service.GetMarketPriceRequest,
) -> project.getCurrentMarketPrice_service.MarketPriceResponse | Response:
    """
    Retrieves the current market price per board foot from an external financial service or a stored value updated periodically. This endpoint helps in keeping the profit calculations up-to-date with market fluctuations. Response should include the latest market price along with the time of the last update.
    """
    try:
        res = await project.getCurrentMarketPrice_service.getCurrentMarketPrice(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/maintenance",
    response_model=project.listMaintenanceRecords_service.GetMaintenanceResponse,
)
async def api_get_listMaintenanceRecords(
    request: project.listMaintenanceRecords_service.GetMaintenanceRequest,
) -> project.listMaintenanceRecords_service.GetMaintenanceResponse | Response:
    """
    Retrieves a list of all maintenance records. Each record will show brief details like machine name, maintenance type, and date. This helps in quickly viewing upcoming or past maintenances.
    """
    try:
        res = await project.listMaintenanceRecords_service.listMaintenanceRecords(
            request
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/orders", response_model=project.createOrder_service.CreateOrderResponse)
async def api_post_createOrder(
    customerId: str, items: List[project.createOrder_service.OrderItem]
) -> project.createOrder_service.CreateOrderResponse | Response:
    """
    Creates a new customer order. It uses inventory data to validate stock before confirming the order. Returns the order ID upon successful creation.
    """
    try:
        res = await project.createOrder_service.createOrder(customerId, items)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/schedules/{scheduleId}",
    response_model=project.updateSchedule_service.ScheduleUpdateResponse,
)
async def api_put_updateSchedule(
    scheduleId: str,
    shiftStartTime: datetime,
    shiftEndTime: datetime,
    equipmentId: str,
    operationPlan: str,
) -> project.updateSchedule_service.ScheduleUpdateResponse | Response:
    """
    Updates an existing schedule based on the given schedule ID. It allows modifications to shift timings, operations plan, and machinery deployment. Maintains synchronization with equipment and resource availability through respective modules.
    """
    try:
        res = await project.updateSchedule_service.updateSchedule(
            scheduleId, shiftStartTime, shiftEndTime, equipmentId, operationPlan
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/orders/calculate-price",
    response_model=project.calculatePrice_service.CalculatePriceResponse,
)
async def api_get_calculatePrice(
    itemType: prisma.enums.ItemType, quantity: int, customerType: str
) -> project.calculatePrice_service.CalculatePriceResponse | Response:
    """
    Provides an estimated cost for a potential order based on current board foot prices and quantity rules. It interacts with both public and private board foot calculators.
    """
    try:
        res = await project.calculatePrice_service.calculatePrice(
            itemType, quantity, customerType
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/orders", response_model=project.listOrders_service.OrdersListResponse)
async def api_get_listOrders(
    request: project.listOrders_service.GetOrdersRequest,
) -> project.listOrders_service.OrdersListResponse | Response:
    """
    Retrieves a list of all customer orders, including order details like customer name, order status, and total cost.
    """
    try:
        res = await project.listOrders_service.listOrders(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/inventory",
    response_model=project.createInventoryItem_service.InventoryItemResponse,
)
async def api_post_createInventoryItem(
    name: str, quantity: int, itemType: prisma.enums.ItemType
) -> project.createInventoryItem_service.InventoryItemResponse | Response:
    """
    Allows creation of new inventory items. This route requires detailed information about the item, such as type, quantity, and status. Only accessible by admins to ensure proper management.
    """
    try:
        res = await project.createInventoryItem_service.createInventoryItem(
            name, quantity, itemType
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/board-foot-calculate",
    response_model=project.calculateBoardFootCost_service.BoardFootCalculateResponse,
)
async def api_post_calculateBoardFootCost(
    diameter: float, treeType: prisma.enums.TreeType, height: float
) -> project.calculateBoardFootCost_service.BoardFootCalculateResponse | Response:
    """
    Calculates the cost based on the input parameters: tree diameter, type, and height. This endpoint uses mathematical formulas to determine the board foot volume, then applies pricing models according to wood type. The result provides a cost estimate crucial for the Sales Module's preliminary cost calculation features.
    """
    try:
        res = await project.calculateBoardFootCost_service.calculateBoardFootCost(
            diameter, treeType, height
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/schedules/{scheduleId}",
    response_model=project.getSchedule_service.FetchScheduleDetailsResponse,
)
async def api_get_getSchedule(
    scheduleId: str,
) -> project.getSchedule_service.FetchScheduleDetailsResponse | Response:
    """
    Fetches specific schedule details by ID. It provides information on the particular operations, shifts assigned, and machinery used for that day. Useful for operational adjustments and real-time updates.
    """
    try:
        res = await project.getSchedule_service.getSchedule(scheduleId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/orders/{orderId}", response_model=project.deleteOrder_service.DeleteOrderResponse
)
async def api_delete_deleteOrder(
    orderId: str,
) -> project.deleteOrder_service.DeleteOrderResponse | Response:
    """
    Deletes a specific order, requiring a re-adjustment in inventory levels. Accessible only by admins to ensure data integrity.
    """
    try:
        res = await project.deleteOrder_service.deleteOrder(orderId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/inventory/{itemId}",
    response_model=project.updateInventoryItem_service.UpdateInventoryItemResponse,
)
async def api_put_updateInventoryItem(
    itemId: str, name: str, quantity: int, itemType: prisma.enums.ItemType
) -> project.updateInventoryItem_service.UpdateInventoryItemResponse | Response:
    """
    Updates existing inventory item data. This is crucial for keeping inventory data up-to-date, reflecting new quantities or material states. Access is restricted to roles that manage inventory.
    """
    try:
        res = await project.updateInventoryItem_service.updateInventoryItem(
            itemId, name, quantity, itemType
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/schedules", response_model=project.createSchedule_service.ScheduleCreationResponse
)
async def api_post_createSchedule(
    shift_details: List[project.createSchedule_service.ShiftDetail],
    equipment_usage: List[project.createSchedule_service.EquipmentUsage],
) -> project.createSchedule_service.ScheduleCreationResponse | Response:
    """
    Creates a new schedule for sawmill operations, including shifts and machinery usage. It checks equipment availability from the Maintenance Tracker and resource availability from Inventory Management before finalizing the schedule. Returns the created schedule details.
    """
    try:
        res = await project.createSchedule_service.createSchedule(
            shift_details, equipment_usage
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/orders/{orderId}", response_model=project.getOrder_service.GetOrderDetailsResponse
)
async def api_get_getOrder(
    orderId: str,
) -> project.getOrder_service.GetOrderDetailsResponse | Response:
    """
    Fetches details of a specific order, including products ordered, quantities, prices, and current status. Useful for order tracking and updates.
    """
    try:
        res = await project.getOrder_service.getOrder(orderId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/inventory/{itemId}",
    response_model=project.getInventoryItem_service.InventoryItemFetchResponse,
)
async def api_get_getInventoryItem(
    itemId: str,
) -> project.getInventoryItem_service.InventoryItemFetchResponse | Response:
    """
    Fetches detailed information for a specific inventory item using the item's unique identifier. Information includes type, quantity, and resource details, useful for sales details and maintenance planning.
    """
    try:
        res = await project.getInventoryItem_service.getInventoryItem(itemId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/maintenance/{recordId}",
    response_model=project.updateMaintenanceRecord_service.MaintenanceUpdateResponse,
)
async def api_put_updateMaintenanceRecord(
    recordId: str,
    maintenanceType: str,
    description: str,
    scheduledDate: Optional[datetime],
    technicianDetails: project.updateMaintenanceRecord_service.EmployeeDetails,
) -> project.updateMaintenanceRecord_service.MaintenanceUpdateResponse | Response:
    """
    Updates an existing maintenance record. It can modify fields like maintenance type, date, and technician details. Ensures records are current and accurate.
    """
    try:
        res = await project.updateMaintenanceRecord_service.updateMaintenanceRecord(
            recordId, maintenanceType, description, scheduledDate, technicianDetails
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/wood-types", response_model=project.fetchWoodTypes_service.GetWoodTypesResponse
)
async def api_get_fetchWoodTypes(
    request: project.fetchWoodTypes_service.GetWoodTypesRequest,
) -> project.fetchWoodTypes_service.GetWoodTypesResponse | Response:
    """
    Retrieves a list of available wood types and their characteristics. This information supports the board foot calculation by providing essential data for accurate cost estimation.
    """
    try:
        res = await project.fetchWoodTypes_service.fetchWoodTypes(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/inventory", response_model=project.listInventoryItems_service.GetInventoryResponse
)
async def api_get_listInventoryItems(
    request: project.listInventoryItems_service.GetInventoryRequest,
) -> project.listInventoryItems_service.GetInventoryResponse | Response:
    """
    Retrieves a list of all inventory items including materials, products, and resources. This endpoint will be accessible to the admin and salesperson roles for order processing and inventory checks.
    """
    try:
        res = await project.listInventoryItems_service.listInventoryItems(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/orders/{orderId}", response_model=project.updateOrder_service.UpdateOrderResponse
)
async def api_put_updateOrder(
    orderId: str, quantity: Optional[int], status: Optional[prisma.enums.OrderStatus]
) -> project.updateOrder_service.UpdateOrderResponse | Response:
    """
    Updates an existing order's details, such as changes in quantity, product or cancellation of the order. Requires checks against inventory for stock adjustments.
    """
    try:
        res = await project.updateOrder_service.updateOrder(orderId, quantity, status)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/calculator/history",
    response_model=project.viewCalculationHistory_service.GetCalculatorHistoryResponse,
)
async def api_get_viewCalculationHistory(
    request: project.viewCalculationHistory_service.GetCalculatorHistoryRequest,
) -> project.viewCalculationHistory_service.GetCalculatorHistoryResponse | Response:
    """
    Provides a record of all previous profit calculations performed through the Board Foot Calculator. Each record should detail the inputs used and the output generated, along with timestamps. This helps in auditing and understanding past operational efficiencies.
    """
    try:
        res = await project.viewCalculationHistory_service.viewCalculationHistory(
            request
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/maintenance/{recordId}/parts",
    response_model=project.useSparePart_service.MaintenancePartsLogResponse,
)
async def api_post_useSparePart(
    recordId: str, parts: List[project.useSparePart_service.PartUsage]
) -> project.useSparePart_service.MaintenancePartsLogResponse | Response:
    """
    Logs the usage of spare parts for a specific maintenance record. It updates inventory levels and ensures accurate tracking of part usage.
    """
    try:
        res = await project.useSparePart_service.useSparePart(recordId, parts)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/calculator/profit",
    response_model=project.calculateProfit_service.ProfitCalculationResponse,
)
async def api_post_calculateProfit(
    treeType: prisma.enums.TreeType, height: float, diameter: float
) -> project.calculateProfit_service.ProfitCalculationResponse | Response:
    """
    This endpoint calculates the potential profit based on the provided tree parameters such as type, height, and diameter. It takes the inputs, applies the board foot calculation formula, and multiplies the result by the current market price per board foot. The endpoint ensures data is in a proper format and integrates with the Sales Module to provide required data. Expected to return profits estimation and potentially useful statistics for planning.
    """
    try:
        res = await project.calculateProfit_service.calculateProfit(
            treeType, height, diameter
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/schedules", response_model=project.listSchedules_service.GetSchedulesResponse
)
async def api_get_listSchedules(
    request: project.listSchedules_service.GetSchedulesRequest,
) -> project.listSchedules_service.GetSchedulesResponse | Response:
    """
    Retrieves a list of all schedules. This endpoint can be used by the management team to overview operational planning and current engagement of resources and employees.
    """
    try:
        res = await project.listSchedules_service.listSchedules(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
