debug 3
Log content:
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
Jobstore Task_plan_1:
    No scheduled jobs
Jobstore default:
    event_update_shibor (trigger: cron[hour='19', minute='0'], next run at: 2020-03-01 19:00:00 CST)
    event_download_index_data (trigger: cron[hour='20', minute='0'], next run at: 2020-03-01 20:00:00 CST)
    event_download_stock_data (trigger: cron[hour='22', minute='0'], next run at: 2020-03-01 22:00:00 CST)
    event_flag_index (trigger: cron[day='3'], next run at: 2020-03-03 00:00:00 CST)
    event_flag_stock (trigger: cron[day='1'], next run at: 2020-04-01 00:00:00 CST)
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
Reason:
任务管理器仍然只向default添加任务
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
Solution：
待解决