import requests
from requests.exceptions import HTTPError
import json
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.ticker as mticks
from datetime import datetime
# plot a figure of a specific size
fig, ax = plt.subplots(1,1,figsize=(18,4))# for storing the date and time
x = []# for storing the stock price
y = []# number of ticks intervals to display for each axis
no_x_intervals = 10
no_y_intervals = 8

# maximum and minimum stock price recorded
max_price = min_price = 0

def animate(i):
    # fetch stock prices
    try:
        url = 'http://localhost:5000/stocks/v1/fetch'
        data = {"Symbol": sys.argv[1]}
        data_json = json.dumps(data)
        headers = {'Content-type':'application/json'}
        response = requests.post(url, data=data_json, 
                   headers=headers)    # Raise an exception if a request is unsuccessful
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  
    except Exception as err:
        print(f'Other error occurred: {err}')  
    else:
        try:
            stock_price = json.loads(response.text)    
        except ValueError as err:  
            print(err)
        else:        
            price = float(stock_price["price"])
    # print(price)    
    global max_price
    global min_price    # store the max and min of the stock price recorded
    max_price = max(price, max_price)    
    min_price = max_price if min_price == 0 else \
                min(price, min_price)
    
    # add the data for x and y-axis    
    x.append(datetime.now().strftime("%H:%M:%S"))
    y.append(price)
    
    # clear the chart and plot again
    ax.clear()
    ax.plot(x, y, linewidth=2,color=sys.argv[2])    # calculate the buffer to add to the top and 
    # bottom of the line chart
    buffer = (max_price - min_price) * 0.20  # 20% of the price
                                             # difference    # set the range of the y-axis
    ax.set_ylim(
        (min(price, min_price) - buffer, 
         max(price, max_price) + buffer)
    )    # display the x-axis ticks with intervals
    ax.xaxis.set_major_locator(       
        # interval spacing of x-ticks        
        mticks.MultipleLocator(len(x) / no_x_intervals))    # display the y-axis ticks with intervals
    ax.yaxis.set_major_locator(
        mticks.MultipleLocator(((max_price - min_price + 1) + \
                                (2*buffer)) / no_y_intervals))    # get the y-ticks and their corresponding labels 
    locs, _ = plt.yticks()    # format the y-axis labels to display 5 decimal places
    plt.yticks(locs, map(lambda x: "%.5f" % x, locs))
    plt.title("Stock Price of " + sys.argv[1])

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()