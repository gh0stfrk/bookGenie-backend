from app.database import IPLog, SessionLocal
from apscheduler.schedulers.asyncio import AsyncIOScheduler


scheduler = AsyncIOScheduler()

@scheduler.scheduled_job("cron", hour=0, minute=0)
async def flush_ip_logs():
    session = SessionLocal()
    session.query(IPLog).delete()
    session.commit()

