from django import template
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule

register = template.Library()

@register.filter
def human_readable_schedule(task):
    if task.interval:
        return f"Every {task.interval.every} {task.interval.period}"
    elif task.crontab:
        c = task.crontab
        
        # Helper to check if a field is a wildcard
        def is_wild(field): return field == '*'

        # Daily at specific time
        if not is_wild(c.minute) and not is_wild(c.hour) and is_wild(c.day_of_week) and is_wild(c.day_of_month) and is_wild(c.month_of_year):
            return f"Daily at {c.hour}:{c.minute.zfill(2)}"
            
        # Hourly at specific minute
        if not is_wild(c.minute) and is_wild(c.hour) and is_wild(c.day_of_week) and is_wild(c.day_of_month) and is_wild(c.month_of_year):
            return f"Hourly at minute {c.minute}"
            
        # Every minute
        if is_wild(c.minute) and is_wild(c.hour) and is_wild(c.day_of_week) and is_wild(c.day_of_month) and is_wild(c.month_of_year):
            return "Every minute"
            
        # Weekly
        if not is_wild(c.minute) and not is_wild(c.hour) and not is_wild(c.day_of_week) and is_wild(c.day_of_month) and is_wild(c.month_of_year):
            return f"Weekly on {c.day_of_week} at {c.hour}:{c.minute.zfill(2)}"
            
        # Monthly
        if not is_wild(c.minute) and not is_wild(c.hour) and is_wild(c.day_of_week) and not is_wild(c.day_of_month) and is_wild(c.month_of_year):
            return f"Monthly on day {c.day_of_month} at {c.hour}:{c.minute.zfill(2)}"

        return f"{c.minute} {c.hour} {c.day_of_week} {c.day_of_month} {c.month_of_year} (Crontab)"
    elif task.solar:
        return f"Solar: {task.solar.event} ({task.solar.latitude}, {task.solar.longitude})"
    elif task.clocked:
        return f"Clocked: {task.clocked.clocked_time}"
    return "Unknown Schedule"

@register.filter
def cron_pretty(cron):
    if not cron:
        return ""
    # Simple converter, can be expanded
    parts = []
    if cron.minute != '*': parts.append(f"at minute {cron.minute}")
    if cron.hour != '*': parts.append(f"past hour {cron.hour}")
    if cron.day_of_week != '*': parts.append(f"on {cron.day_of_week}")
    
    if not parts:
        return "Every minute"
    return ", ".join(parts)
