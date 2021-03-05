import datetime
import csv
import numpy as np
from scipy.stats import boxcox
from scipy.special  import inv_boxcox

import os
import sys
import psycopg2

from datetime import datetime as dt

print("WORKFLOW START [BOXCOX] :", dt.isoformat(dt.utcnow()))

idValue = (sys.argv[1])
print("idValue : %(idValue)s")

timeValue = (sys.argv[2])
print("timeValue : %(timeValue)s")

cdate = (sys.argv[3])
print("cdate : %(cdate)s")

sigma = float(sys.argv[4])
print("sigma : %(sigma)s")

connParam = "dbname = 'db' user = 'user' host = '192.168.10.1' password = 'paranlee'"
conn = psycopg2.connect(connParam)
cur = conn.cursor()

sql = """SELECT value 
        FROM ts_bg_alarm_outlier_threshold_data 
        WHERE cdate = %(cdate)s 
            AND idValue = %(idValue)s 
            AND timeValue = %(timeValue)s ;"""

cur.execute(sql)

result = [r[0] for r in cur.fetchall()]

inputSeries = np.array(result, dtype=float)
print("inputSeries: ", inputSeries)

# tryboxcox transformation
try:
    #inputSeries = np.array(list_file,dtype=float)
    transformed, lamda = boxcox(inputSeries)

    print("transformed output : ", transformed)

    print("max lamda value : ", lamda)

    print(transformed[0])
    print(transformed[1])

    stddev = np.std(transformed)
    avg = np.mean(transformed)

    orgAvg = np.mean(inputSeries)
    orgStd = np.std(inputSeries)
 
    print("avg value : %(avg)s")
    print("std value : %(stddev)s")

    print("orgAvg value : %(orgAvg)s")
    print("orgStd value : %(orgStd)s")

    print("sigma value : %(sigma)s")

    # up, down boundary
    up = avg + (stddev * sigma)
    down = avg - (stddev * sigma)

    orgUp = orgAvg + (orgStd * sigma)
    orgDown = orgAvg - (orgStd * sigma)

    print("up bodundary output : %(up)s")
    print("down boundary output : %(down)s")

    print("orgUp output : %(orgUp)s")
    print("orgDown output : %(orgDown)s")

    #inverse up,down
    invup = inv_boxcox(up, lamda)
    invdown = inv_boxcox(down, lamda)

    print("invup output : %(invup)s")
    print("invdown output : %(invdown)s")

    invup2 = ((up * lamda) ** (1 / lamda))
    invdown2 = ((down * lamda) ** (1 / lamda))

    print("invup2 output : %(invup2)s")
    print("invdown2 output : %(invdown2)s")

    if str(invup) == 'nan' or str(invup) == 'inf':
        invup = orgUp

    if str(invdown) == 'nan' or str(invdown) == 'inf':
        invdown = orgDown

    invup = orgUp
    invdown = orgDown


except:
    print('except')
    orgAvg = np.mean(inputSeries)
    orgStd = np.std(inputSeries)

    orgUp = orgAvg   (orgStd * sigma)
    orgDown = orgAvg - (orgStd * sigma)

    invup = orgUp
    invdown = orgDown

    print(orgAvg)
    print(orgStd)

    if str(invup) == 'nan' or str(invup) == 'inf':
        invup = psycopg2.extensions.AsIs('NULL')

    if str(invdown) == 'nan' or str(invdown) == 'inf':
        invdown = psycopg2.extensions.AsIs('NULL')

#minus change 0
#if invup < 0:
# invup = 0
#if invdown < 0:
# invdown = 0

# threshold update
cur.execute("update ts_bg_alarm_outlier_threshold set threshold_min = %s ,threshold_max = %s where cdate = %s and idValue = %s and timeValue = %s;",(invdown, invup, cdate, idValue, timeValue))
conn.commit()

print("WORKFLOW END [BOXCOX] :", dt.isoformat(dt.utcnow()))