from apscheduler.schedulers.background import BackgroundScheduler
from backend.services.ApplicationService import ApplicationService

class SchedulerService:
    def __init__(self, application_service: ApplicationService):
        self.scheduler = BackgroundScheduler()
        self.application_service = application_service

    def setup_jobs(self):
        self.scheduler.add_job(
            self.application_service.reject_old_applications,
            'cron',
            hour=0,  # Run at midnight
            minute=0
        )

    def start(self):
        self.setup_jobs()
        self.scheduler.start()

    def stop(self):
        self.scheduler.shutdown()