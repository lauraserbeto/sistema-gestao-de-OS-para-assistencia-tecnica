from app.repositories.report_repository import ReportRepository


class ReportService:
    def __init__(self, repository: ReportRepository):
        self.repository = repository

    def orders_by_status(self):
        return self.repository.orders_by_status()

    def late_orders(self):
        return self.repository.late_orders()

    def top_technicians(self):
        return self.repository.top_technicians()

    def most_used_parts(self):
        return self.repository.most_used_parts()

    def average_service_time(self):
        return self.repository.average_service_time()