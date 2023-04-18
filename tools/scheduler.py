import asyncio
import time
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_MISSED, EVENT_JOB_EXECUTED, JobEvent, JobExecutionEvent, \
    EVENT_JOB_ADDED, EVENT_JOB_SUBMITTED, EVENT_JOB_REMOVED, EVENT_JOB_MAX_INSTANCES, EVENT_JOB_MODIFIED
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger
from pymongo import MongoClient

from configs import settings

event_map = {
    2 ** 0: "EVENT_SCHEDULER_STARTED",
    2 ** 0: "EVENT_SCHEDULER_START",
    2 ** 1: "EVENT_SCHEDULER_SHUTDOWN",
    2 ** 2: "EVENT_SCHEDULER_PAUSED",
    2 ** 3: "EVENT_SCHEDULER_RESUMED",
    2 ** 4: "EVENT_EXECUTOR_ADDED",
    2 ** 5: "EVENT_EXECUTOR_REMOVED",
    2 ** 6: "EVENT_JOBSTORE_ADDED",
    2 ** 7: "EVENT_JOBSTORE_REMOVED",
    2 ** 8: "EVENT_ALL_JOBS_REMOVED",
    2 ** 9: "EVENT_JOB_ADDED",
    2 ** 10: "EVENT_JOB_REMOVED",
    2 ** 11: "EVENT_JOB_MODIFIED",
    2 ** 12: "EVENT_JOB_EXECUTED",
    2 ** 13: "EVENT_JOB_ERROR",
    2 ** 14: "EVENT_JOB_MISSED",
    2 ** 15: "EVENT_JOB_SUBMITTED",
    2 ** 16: "EVENT_JOB_MAX_INSTANCES"
}


def create_scheduler(store_mongodb_url) -> AsyncIOScheduler:
    def job_listener(event: JobExecutionEvent):
        if getattr(event, "exception", None):
            logger.error(
                f"[Scheduler] [{event.job_id}] [{event_map.get(event.code, event.code)}]|{event.exception}|{event.traceback}")
        else:
            logger.info(
                f'[Scheduler] [{event.job_id}] [{event_map.get(event.code, event.code)}]')

    scheduler: AsyncIOScheduler = AsyncIOScheduler(
        jobstores={
            'default': MongoDBJobStore(client=MongoClient(store_mongodb_url),
                                       database='scheduler' if settings.env != 'LOCAL' else "scheduler_dev",
                                       collection='jobs'),
            'memory': MemoryJobStore()},
        max_workers=200
    )
    scheduler.add_listener(job_listener,
                           mask=(EVENT_JOB_ADDED | EVENT_JOB_REMOVED | EVENT_JOB_MODIFIED | EVENT_JOB_EXECUTED |
                                 EVENT_JOB_ERROR | EVENT_JOB_MISSED | EVENT_JOB_SUBMITTED | EVENT_JOB_MAX_INSTANCES))
    return scheduler


def task_job():
    print(time.time())


async def test():
    scheduler = create_scheduler(settings.mongodb)
    scheduler.start()
    scheduler.remove_all_jobs()
    scheduler.print_jobs()
    # scheduler.add_job(func=task_job, trigger=interval.IntervalTrigger(seconds=5, timezone=pytz.UTC),
    #                   misfire_grace_time=10)
    while True:
        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(test())
