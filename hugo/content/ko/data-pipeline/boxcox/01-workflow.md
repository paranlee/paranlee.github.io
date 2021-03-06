+++
author = "Paran Lee"
title = "Boxcox transformation on workflow"
date = "2021-03-01"
description = "Boxcox transformation, perspective of workflow"
weight = 2
tags = [
    "markdown",
    "css",
    "html",
    "themes",
]
categories = [
    "themes",
    "syntax",
]
series = ["Data pipeline"]
+++

## Concept

몇가지 개념정리 및 코드를 보고 진행합니다.

## Outlier removal workflow

차분(Difference):

    sort 후 각 항목의 차이 값

    차분 값의 배열을 만들 수 있음.

사분위수(Quartile):

    데이터를 가장 작은 수부터 가장 큰 수까지 크기가 커지는 순서대로 정렬하였을 때,
    1/4, 2/4, 3/4 위치에 있는 수를 말한다. 

    각각 1사분위수, 2사분위수, 3사분위수라고 한다. 

    1/4의 위치란 전체 데이터의 수가 만약 100개이면 25번째 순서, 즉 하위 25%를 말한다. 
    따라서 2사분위수는 중앙값과 같다.

    때로는 위치를 1/100 단위로 나눈 백분위수(percentile)을 사용하기도 한다. 1사분위수는 25% 백분위수와 같다.

    np.percentile(x, 0)  # 최소값
    np.percentile(x, 25)  # 1사분위 수
    np.percentile(x, 50)  # 2사분위 수
    np.percentile(x, 75)  # 3사분위 수
    np.percentile(x, 100)  # 최댓값

아래는 위의 설명한 개념을 이용한 예제 프로그램입니다.

#### Oulier removal using diffrence series
{{< highlight py >}}
  
# Set lower and upper bound of a sequence
# Percentile -> Difference -> x sigma
 
import numpy as np
import pandas ad pd

"""
# numpy.argmin
# min(), max() : 최소, 최대값을 구하기. 
# argmin(), argmax() : 최소, 최대값이 존재하는 위치(인덱스)를 구하기.

# numpy.arange([start, ] stop, [step, ] dtype=None)
numpy 모듈의 arange 함수는 반열린구간 [start, stop) 에서 
step 의 크기만큼 일정하게 떨어져 있는 숫자들을 array 형태로 반환해 주는 함수다.

# numpy.mean
평균 구하기

# numpy.diff(arr, [n])
n order 차분을 구함

"""

"""
@self :
@series : 양의 실수 값으로 이루어진 1차원 배열
@scale : 
@cut_pt : 
@cut_ratio : 정규 분포로 변환된 데이터에서 선택할 표준 편차(시그마)값

"""

class Self:

    def __init__(self):
        self.series = np.array([]);
        
    def setSeries(arr)
        self.series = np.array(arr);

    def calc_bound_from_dist(self, series = self.series, scale = 1000, cut_pt = 10, cut_ratio = 2):
        
        unit = 100 / scale
        center = int(scale / 2)
        cut_point = int(cut_pt / unit) if cut_pt / unit > 1 else 1 # 100
        
        # np.percentile(1000, np.arange(0, 100.1, 0.1))
        # np.percentile(1000, [   0.     0.1    0.2 ...,   99.8   99.9  100. ])
        percentiles = np.percentile(series, np.arange(0, 100 + unit, unit))
        
        # nonstationary process -> stationary process
        
        # TODO : Operator Overloading
        # percentiles[1:1001] - percentiles[0:1000]
        #   -> e(n+1) - e(n) -> 1 dimensional array
        # 1st order differincing
        diff = percentiles[1:scale + 1] - percentiles[0:scale]
        # diff = np.diff(percentiles)
        
        # TODO : Operator Overloading 
        # 1e-6 delta less than (>) filter -> 1 dimensional array
        diff_nnz_idx = np.abs(diff) > 1e-6 # 1 * 10^(-6)
        
        # Fix code to cpu caching
        
        """ Upper Bound Operation """
        
        ev_upper_range = np.arange(center, scale - cut_point + 1, 1) # [500, 501, ... 900]
        diff_ev_upper_part = diff[ev_upper_range][diff_nnz_idx[ev_upper_range]]
        
        upper_bound_diff = np.mean(diff_ev_upper_part) + np.std(diff_ev_upper_part) * cut_ratio
        
        # upper
        upper_bound_idx = np.argmax(diff[center:] > upper_bound_diff)
            
        if upper_bound_idx == 0 or upper_bound_idx == scale-center:
            upper_bound_idx = scale - 1
        else:
            upper_bound_idx += center
            
        upper_bound = percentiles[upper_bound_idx]
        
        """ Lower Bound Operation """
                
        ev_lower_range = np.arange(cut_point, center + 1, 1) # [100, 101, ... 500]
        diff_ev_lower_part = diff[ev_lower_range][diff_nnz_idx[ev_lower_range]]
        
        lower_bound_diff = np.mean(diff_ev_lower_part) + np.std(diff_ev_lower_part) * cut_ratio
                
        # lower
        lower_bound_idx = -np.argmax(diff[center::-1] > lower_bound_diff)
            
        if lower_bound_idx == 0 or lower_bound_idx == -center:
            lower_bound_idx = 1
        else:
            lower_bound_idx += center
                
        lower_bound = percentiles[lower_bound_idx]

        return upper_bound, lower_bound

{{< /highlight >}}


## Boxcox Transformation

boxcox transformation

    복잡한 지수함수의 승수의 해를 뉴턴 메서드로 구하고 이를 정규분포로 변환합니다.

무작위 값으로 boxcox 값이 얼마나 정규분포로 잘 바꿔주는지

[box-cox-transformation-using-python](https://www.geeksforgeeks.org/box-cox-transformation-using-python/)에 한눈에 보기 쉬운 예제가 있습니다.


아래 예제는 실제 측정값을 예제로 하는 예시입니다.

C.Doom의 Cygnus 방향으로 47 개의 별을 포함하는 성단 CYG OB1의 Hertzsprung-Russell Diagram 실측 데이터입니다.

첫 번째 변수는 별 표면에서 유효 온도의 로그 (log.Te)이고 두 번째 변수는 빛 강도의 로그(log.light)입니다.

아래의 예제에서는 log.Te 만 데이터로 사용합니다.

[원본 데이터](https://www.rdocumentation.org/packages/robustbase/versions/0.93-6/topics/starsCYG)

[원본 데이터 csv](https://forge.scilab.org/index.php/p/rdataset/source/tree/368b19abcb4292c56e4f21079f750eb76b325907/csv/robustbase/starsCYG.csv)

예제를 돌리기 위해서 아나콘다 프레임워크를 설치하면 편리합니다.

아래는 예제에서는 [scipy.stats.boxcox](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.boxcox.html) 라이브러리를 사용합니다.

    scipy.stats.boxcox(x, lmbda=None, alpha=None)[source]
    Return a dataset transformed by a Box-Cox power transformation.

    Parameters
        xndarray
        Input array. Must be positive 1-dimensional. Must not be constant.

        lmbda{None, scalar}, optional
        If lmbda is not None, do the transformation for that value.

        If lmbda is None, find the lambda that maximizes the log-likelihood function and return it as the second output argument.

        alpha{None, float}, optional
        If alpha is not None, return the 100 * (1-alpha)% confidence interval for lmbda as the third output argument. Must be between 0.0 and 1.0.

    Returns
        boxcoxndarray
        Box-Cox power transformed array.

        maxlogfloat, optional
        If the lmbda parameter is None, the second returned argument is the lambda that maximizes the log-likelihood function.

        (min_ci, max_ci)tuple of float, optional
        If lmbda parameter is None and alpha is not None, this returned tuple of floats represents the minimum and maximum confidence limits given alpha.

[비정상 확률 과정을 정상 확률 과정으로 변환하기](https://datascienceschool.net/view-notebook/3f485c426a4b49fc9de95a02137ca6b4/)

#### Boxcox transformation example

{{< highlight py >}}

import statsmodels.api as sm
import matplotlib.pyplot as plt
from scipy.stats import boxcox
import seaborn as sns
import dautil as dl
import pandas_datareader as pd
import numpy as np
# import csv

#from IPython.display import HTML

# Load the data and transform it as follows :
context = dl.nb.Context('normalizing_boxcox')
lr = dl.nb.LatexRenderer(chapter=4, start=3, context=context)
lr.render(r'y_i^{(\lambda)} = \begin{cases} \dfrac{y_i^\lambda - 1}{\lambda} & \text{if } \lambda \neq 0, \\[8pt] \ln{(y_i)} & \text{if } \lambda = 0, \end{cases} ')

starsCYG = sm.datasets.get_rdataset("starsCYG", "robustbase", cache=True).data

whichData = 'log.Te'

# Data must be positive
# Data must be 1-dimensional.
transformed, lamda = boxcox(starsCYG[whichData])

# export CSV
#with open('test', 'w', newline='', encoding='utf-8') as csv_file:
    #writer = csv.writer(transformed, delimiter=',')
    #writer.writerow('my_utf8_string')

print("1. input data : ")
print(starsCYG)
print(type(starsCYG))

np.savetxt('./input_data.txt'
   , (starsCYG)
   , header='--input data start--'
   , footer='--input data end--'
   , fmt='%1.2f')

print("\n\n")

print("2. input data [%s] : " %whichData)
print(starsCYG[whichData])
print(type(starsCYG[whichData]))

np.savetxt('./input_data_x.txt'
   , (starsCYG)
   , header='--input data start--'
   , footer='--input data end--'
   , fmt='%1.2f')

print("\n\n")

print("3. transformed output : ")
print(transformed)
print(type(transformed))

print("max lamda value : ")
print(lamda)
print(type(lamda))

print("\n\n")

np.savetxt('D:/PythonProject/output_data_x.txt'
   , (transformed)
   , header='--output data start--'
   , footer='--output data end--'
   , fmt='%1.2f')

#region Plot
# Display the Q - Q plots and the distribution as follows :

#"""
sp = dl.plotting.Subplotter(2, 2, context)
sp.label()
sm.qqplot(starsCYG[whichData], fit=True, line='s', ax=sp.ax)

sp.label(advance=True)
sm.qqplot(transformed, fit=True, line='s', ax=sp.ax)

sp.label(advance=True)
sns.distplot(starsCYG[whichData], ax=sp.ax)

sp.label(advance=True)
sns.distplot(transformed, ax=sp.ax)                                       
plt.tight_layout()
plt.show()

#"""

#endregion Plot

{{< /highlight >}}


다음은 postgres 에 적재하는 예시를 보겠습니다.

Postgres 연동은 [Citus membership-manager.py](https://github.com/citusdata/membership-manager/blob/master/manager.py) 를 참고했습니다.

## Boxcox transformation batch process example on postgres

{{< highlight py>}}

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

    print("transformed: ", transformed[0], transformed[1])

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

    orgUp = orgAvg + (orgStd * sigma)
    orgDown = orgAvg - (orgStd * sigma)

    invup = orgUp
    invdown = orgDown

    print(orgAvg)
    print(orgStd)

    if str(invup) == 'nan' or str(invup) == 'inf':
        invup = psycopg2.extensions.AsIs('NULL')

    if str(invdown) == 'nan' or str(invdown) == 'inf':
        invdown = psycopg2.extensions.AsIs('NULL')

# minus change 0
# if invup < 0:
#     invup = 0
# if invdown < 0:
#     invdown = 0

# threshold update

sql = """UPDATE
        outlier_threshold_table
    SET threshold_min = %(invdown)s,
        threshold_max = %(invup)s 
    WHERE 1=1
        AND cdate = %(cdate)s 
        AND idValue = %(idValue)s
        AND timeValue = %(timeValue)s ;"""

cur.execute(sql)

conn.commit()

print("WORKFLOW END [BOXCOX] :", dt.isoformat(dt.utcnow()))

{{< /highlight >}}

PG 에는 내장 함수에 Boxcox transformation 이 없고, 

부동소수점에 대한 예외처리가 좀 더 편리하게 할 수 있어, 

PL/SQL 프로시저로 구현하지 않고, Python3 로 구현한 배치 프로그램 예시를 구현해보았습니다.

## Summary

최종적으로 데이터 적재를 위해서는

1. 이상점 추출 및 제외하기

2. 정규분포 변환 후 표준편차로 적재할 데이터의 범위 설정, 역변환한 값을 적재하기

크게 2가지 워크 플로우로 이루어지는 것을 확인했습니다.

