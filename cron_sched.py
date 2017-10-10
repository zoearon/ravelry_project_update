from crontab import CronTab
 
my_cron = CronTab(user="vagrant")
job = my_cron.new(command='python ~/src/project/reminders.py')
job.hour.every(1)
 
my_cron.write()
