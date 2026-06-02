from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.report_repository import ReportRepository
from app.services.report_service import ReportService

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/orders-by-status")
def orders_by_status(db: Session = Depends(get_db)):
    service = ReportService(ReportRepository(db))

    return [
        {
            "status": row.status,
            "total": row.total
        }
        for row in service.orders_by_status()
    ]


@router.get("/late-orders")
def late_orders(db: Session = Depends(get_db)):
    service = ReportService(ReportRepository(db))
    return service.late_orders()


@router.get("/top-technicians")
def top_technicians(db: Session = Depends(get_db)):
    service = ReportService(ReportRepository(db))

    return [
        {
            "tecnico": row.name,
            "total": row.total
        }
        for row in service.top_technicians()
    ]


@router.get("/most-used-parts")
def most_used_parts(db: Session = Depends(get_db)):
    service = ReportService(ReportRepository(db))

    return [
        {
            "peca": row.nome,
            "quantidade": row.total
        }
        for row in service.most_used_parts()
    ]


@router.get("/average-service-time")
def average_service_time(db: Session = Depends(get_db)):
    service = ReportService(ReportRepository(db))

    return {
        "tempo_medio_horas": service.average_service_time()
    }