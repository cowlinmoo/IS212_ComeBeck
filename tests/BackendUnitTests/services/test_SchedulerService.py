import pytest
from unittest.mock import MagicMock
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.cron.expressions import AllExpression

from backend.services.ApplicationService import ApplicationService
from backend.services.SchedulerService import SchedulerService  # Update the import based on your structure


@pytest.fixture
def application_service_mock():
    """Fixture to create a mock ApplicationService."""
    return MagicMock(spec=ApplicationService)


@pytest.fixture
def scheduler_service(application_service_mock):
    """Fixture to create a SchedulerService with a mock ApplicationService."""
    return SchedulerService(application_service=application_service_mock)


def test_scheduler_initialization(scheduler_service):
    """Test that SchedulerService initializes with a BackgroundScheduler."""
    assert isinstance(scheduler_service.scheduler, BackgroundScheduler)
    assert scheduler_service.application_service is not None


def test_setup_jobs(scheduler_service):
    """Test that the job is set up correctly."""
    scheduler_service.setup_jobs()

    # Check that the job is scheduled
    jobs = scheduler_service.scheduler.get_jobs()
    assert len(jobs) == 1  # There should be one job scheduled
    assert jobs[
               0].func == scheduler_service.application_service.reject_old_applications  # Ensure the correct function is scheduled

    # Check that it's a CronTrigger
    assert isinstance(jobs[0].trigger, CronTrigger)  # Ensure it's a CronTrigger

    # Ensure it runs at midnight
    trigger = jobs[0].trigger
    assert trigger.fields[0].expressions == [0] or isinstance(trigger.fields[0].expressions[0],
                                                              AllExpression)  # Check hour
    assert trigger.fields[1].expressions == [0] or isinstance(trigger.fields[1].expressions[0],
                                                              AllExpression)  # Check minute


def test_start(scheduler_service):
    """Test that start sets up jobs and starts the scheduler."""
    scheduler_service.start()

    # Check that jobs are set up
    jobs = scheduler_service.scheduler.get_jobs()
    assert len(jobs) == 1  # There should be one job scheduled

    # Check that the scheduler is running
    assert scheduler_service.scheduler.running


def test_stop(scheduler_service):
    """Test that stop shuts down the scheduler."""
    scheduler_service.start()  # Start the scheduler first
    scheduler_service.stop()  # Now stop it

    # Check that the scheduler is no longer running
    assert not scheduler_service.scheduler.running
