from crontab import CronTab
 
my_cron = CronTab(user="vagrant")
job = my_cron.new(command='env > src/cronenv')
job.hour.every(1)
 
my_cron.write()
