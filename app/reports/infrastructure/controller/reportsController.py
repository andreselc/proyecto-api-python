from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.orders.infrastructure.repository.orderRepository import OrderRepository
from app.orders.application.services.getTotalSales import GetTotalSalesService
from app.orders.application.services.getSalesByProductId import GetSalesByProductIdService
from app.orders.application.services.getTotalProfit import GetTotalProfitService
from app.orders.application.services.getProfitByProductId import GetProfitByProductIdService
from app.orders.application.services.getTopSellingProductsService import GetTopSellingProductsService
from app.reports.infrastructure.db import database
from app.users.auth.Role_Checker import RoleChecker
router = APIRouter(
    tags=["Reports"]
)

@router.get("/reports/sales/total", status_code=status.HTTP_200_OK, dependencies=[Depends(RoleChecker(["manager"]))])
async def get_total_sales(session: AsyncSession = Depends(database.get_session)):
    repo = OrderRepository(session)
    sales_service = GetTotalSalesService(repo)
    try:
        total_sales = await sales_service.get_total_sales()
        if total_sales == 1:
            message = f"Se ha realizado {total_sales} venta total"
        else:
            message = f"Se han realizado {total_sales} ventas totales"
        return {"message": message}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/reports/sales/{product_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(RoleChecker(["manager"]))])
async def get_sales_by_product_id(product_id: str, session: AsyncSession = Depends(database.get_session)):
    repo = OrderRepository(session)
    sales_service = GetSalesByProductIdService(repo)
    try:
        total_sales = await sales_service.get_sales_by_product_id(product_id)
        if total_sales == 1:
            message = f"Se ha realizado {total_sales} venta total para el producto con ID {product_id}"
        else:
            message = f"Se han realizado {total_sales} ventas totales para el producto con ID {product_id}"
        return {"message": message}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/reports/profit/total", status_code=status.HTTP_200_OK, dependencies=[Depends(RoleChecker(["manager"]))])
async def get_total_profit(session: AsyncSession = Depends(database.get_session)):
    repo = OrderRepository(session)
    profit_service = GetTotalProfitService(repo)
    try:
        total_profit = await profit_service.get_total_profit()
        return {"message": f"Las ganancias totales son {total_profit}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/reports/profit/{product_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(RoleChecker(["manager"]))])
async def get_profit_by_product_id(product_id: str, session: AsyncSession = Depends(database.get_session)):
    repo = OrderRepository(session)
    profit_service = GetProfitByProductIdService(repo)
    try:
        total_profit = await profit_service.get_profit_by_product_id(product_id)
        return {"message": f"Las ganancias totales para el producto con ID {product_id} son {total_profit}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/reports/products/top", status_code=status.HTTP_200_OK, dependencies=[Depends(RoleChecker(["manager"]))])
async def get_top_selling_products(limit: int = Query(10), session: AsyncSession = Depends(database.get_session)):
    repo = OrderRepository(session)
    top_selling_service = GetTopSellingProductsService(repo)
    try:
        top_selling_products = await top_selling_service.get_top_selling_products(limit)
        return {"top_selling_products": top_selling_products}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))