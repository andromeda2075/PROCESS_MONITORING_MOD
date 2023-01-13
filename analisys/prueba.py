import numpy
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

# https://www.earthdatascience.org/courses/use-data-open-source-python/use-time-series-data-in-python/date-time-types-in-pandas-python/customize-dates-matplotlib-plots-python/
# https://naps.com.mx/blog/uso-de-query-con-pandas-en-python/
# https://www.programcreek.com/python/example/61483/matplotlib.dates.DateFormatter
# https://www.geeksforgeeks.org/matplotlib-dates-dateformatter-class-in-python/
# http://blog.espol.edu.ec/telg1001/senales-escalon-%CE%BCt-e-impulso-%CE%B4t/
# 
'''
                                        uniquename  event   pid
timestamp_occured                                              
2022-12-12 19:39:27  fm57-c01a_GuiDisplay-run_1144      3  1144
2022-12-12 19:39:28  fm57-c01a_GuiDisplay-run_1144      0  1144
2022-12-12 23:08:14  fm57-c01a_GuiDisplay-run_1144      3  1144
2022-12-12 23:08:15  fm57-c01a_GuiDisplay-run_1144      1  1144
2022-12-12 23:08:16  fm57-c01a_GuiDisplay-run_1144      0  1144

'''


total_bars = 25
numpy.random.seed(total_bars)

#dates = pandas.date_range('3/4/2020',periods=total_bars,freq='m')
dates=pd.date_range(start='19:39:27',periods=total_bars,freq='s')
print(dates)



diff = pd.DataFrame(data=numpy.random.randn(total_bars),index=dates,columns=['A'])
figure, axes = plt.subplots(figsize=(10, 6))
axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

axes.bar(diff.index,diff['A'],width=25,align='center')





