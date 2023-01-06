import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
from datetime import datetime, timedelta
'''
goals = [0, 1, 2, 3, 4, 5, 6]
times = [
    datetime.time(18, 0,35), datetime.time(18, 18), datetime.time(18, 28),
    datetime.time(18, 38), datetime.time(19, 5), datetime.time(19, 11),
    datetime.time(19, 15)
]
print(times[0])
ax = plt.axes()
# Convert datetime.time objects into datetime.datetime objects by adding a date
# to the time
datetimes = [datetime.datetime.combine(datetime.date.today(), t) for t in times]
print(datetimes[0])
ax.plot(datetimes, goals)
ax.set_title('2018 FIFA World Cup Final')
ax.set_ylabel('Goals')
ax.set_xlabel('Time of Day (MSK; UTC+3)')
# Re-format the x-axis
fmt = mdates.DateFormatter('%M:%S')
ax.xaxis.set_major_formatter(fmt)

plt.show()

'''


'''# Draw Plot
def plot_df(df, x, y, title="", xlabel='Date', ylabel='Value', dpi=100):
    plt.figure(figsize=(16,5), dpi=dpi)
    plt.plot(x, y, color='tab:red')
    plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
    plt.show()

plot_df(df, x=df.index, y=df.value, title='Monthly anti-diabetic drug sales in Australia from 1992 to 2008.')
'''

intervalos = [
        ['2022-12-12 14:04:00' ,'2022-12-12 16:39:00'],
        ['2022-12-12 17:05:00' ,'2022-12-12 19:06:00'],
        ['2022-12-12 20:48:00' ,'2022-12-12 22:52:00'],
        ['2022-12-12 23:34:00' ,'2022-12-13 04:35:00'],
        ['2022-12-13 05:02:00' ,'2022-12-13 07:12:00'],
        ['2022-12-13 08:21:00' ,'2022-12-13 10:48:00'],
        ['2022-12-13 13:59:00' ,'2022-12-13 16:35:00'],
        ['2022-12-13 17:53:00' ,'2022-12-13 19:25:00'],
        ['2022-12-13 20:40:00' ,'2022-12-14 00:23:00'],
        ['2022-12-14 01:13:00' ,'2022-12-14 03:31:00'],
        ['2022-12-14 04:27:00' ,'2022-12-14 07:55:00'],
        ['2022-12-14 08:20:00' ,'2022-12-14 08:43:00'],
        ['2022-12-14 09:10:00' ,'2022-12-14 13:02:00'],
        ['2022-12-14 13:49:00' ,'2022-12-14 16:14:00'],
        ['2022-12-14 16:16:00' ,'2022-12-14 17:53:00'],
        ['2022-12-14 19:53:00' ,'2022-12-14 21:55:00'],
        ['2022-12-14 22:44:00' ,'2022-12-15 04:15:00']
    ]
'''
ini_time_for_now = datetime.now()

print(ini_time_for_now)
print(type(ini_time_for_now))
# printing initial_date
print ("initial_date", str(ini_time_for_now))

future_date_after_2yrs = ini_time_for_now + timedelta(days = 730)

future_date_after_2days = ini_time_for_now + timedelta(days = 2)

'''

time_end='14/12/22 22:44:30'
format_data= "%d/%m/%y %H:%M:%S"
end_time = datetime.strptime(time_end, format_data)
print(type(end_time))
time= end_time+timedelta(seconds=20)
print(time)




# printing calculated future_dates
# print('future_date_after_2yrs:', str(future_date_after_2yrs))
# print('future_date_after_2days:', str(future_date_after_2days))