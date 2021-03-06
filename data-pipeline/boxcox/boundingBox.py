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