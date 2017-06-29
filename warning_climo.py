#!/usr/bin/env python
''' Plots bar charts of warning climatology using a CSV from the NWS warning climatology website

This program will read in a CSV file (format: warning type,issuance time) of all warnings issued
by a WFO (multiple WFOs may work, but is untested). The script will generate a bar chart of the 
number of warnings issued for each calendar date of the year.

Version history:
1.0 (2017 June 29): initial build.
'''

import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
import collections

__author__ = "Jason W. Godwin"
__copyright__ = "Public Domain"
__credits__ = ""

__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Jason W. Godwin"
__email__ = "jasonwgodwin@gmail.com"
__status__ = "Production"

# user settings
warnings_file = 'fwd_warnings.csv'              # warnings file (type in column 0, issuance in column 1)
wfo = 'FWD'                                     # weather forecast office
start = '1987'                                  # beginning of period of record (string)
end = '2016'                                    # end of period of record (string)
product_type = ['SVR','TOR','FFW','all']        # warning types (you probably won't change this)

# import CSV file
df = pd.read_csv(warnings_file)
products = list(df['PRODUCT'])
issuances = list(df['ISSUANCE'])

# convert issuances into datetimes
issuances_dt = [datetime.datetime.strptime(x,"%m/%d/%y %H:%M") for x in issuances]

# get all calendar dates
issuances_cdates = [datetime.datetime.strftime(y,"%m/%d") for y in issuances_dt]

# combine type and calendar date into a list of tuples
issuance_cdates_products = []
for i in range(len(products)):
    issuance_cdates_products.append((products[i],issuances_cdates[i]))

# find count for each calendar date
all_date_count = {}
# loop through product types
for j in product_type:
    if j != 'all':
        date_count = {}
        # loop through months
        for m in range(1,13):
            # assign correct number of dates to each month
            if m in [1,3,5,7,8,10,12]:
                days = 31
            elif m in [4,6,9,11]:
                days = 30
            elif m == 2:
                days = 29
            else:
                raise Exception("Invalid month!")

            # loop through dates
            for d in range(1,days+1):
                if m < 10:
                    month = "0" + str(m)
                else:
                    month = str(m)
                if d < 10:
                    day = "0" + str(d)
                else:
                    day = str(d)

                # create date string
                date = month + "/" + day

                # count number of (product,date) matches
                date_count[date] = issuance_cdates_products.count((j,date))
                # to create the initial key, we use a try/except block
                try:
                    all_date_count[date] = all_date_count[date] + date_count[date]
                except KeyError:
                    all_date_count[date] = date_count[date]

    # assign the date count to all for the final plot
    if j == 'all':
        date_count = all_date_count

    # sort the dictionary to make it plottable
    date_count = collections.OrderedDict(sorted(date_count.items()))

    # create and save the plot
    plt.clf()
    plt.bar(np.arange(len(date_count)),date_count.values(),color='k')
    plt.xticks(np.arange(len(date_count))[::30],date_count.keys()[::30],rotation=90)
    plt.xlim([0,365])
    plt.ylim([0,300])
    plt.suptitle("WFO %s %s Climatology" % (wfo,j))
    plt.title("%s-%s" % (start,end))
    plt.xlabel("Calendar Date")
    plt.ylabel("Warnings issued (%s)" % j)
    plt.grid()
    plt.savefig("%s_%s_climo.png" % (wfo,j),bbox_inches="tight")
