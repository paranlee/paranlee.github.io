+++
author = "Paran Lee"
title = "Why project needed Boxcox transformation?"
date = "2021-03-01"
description = "Using Boxcox transformation in data workflow"
weight = 1
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
series = ["Themes Guide"]
+++

## Why use Boxcox transformation, perspective of workflow

값들의 차분 배열 (sort 후 뒤에 친구 값이랑 나랑 차이만 쏙)

→ boxcox transformation (복잡한 지수함수의 승수의 해를 뉴턴 메서드로 구하고 이를 정규분포로 변환)

→ 정규분포 6 σ (적당한 값 추리기 좋다)

→ 평범한 놈들 그래 니들을 원했어 ㅇㅇ

#### Definiotion of the Boxcox transformation

선두 그룹에 값이 몰려 있는 경우처럼 통계적으로 접근하는 값들이 불균일한 산포를 이룰 경우, 

이 값들을 정규분포 관점으로 접근하고자 할 때 Boxcox transformation 을 사용합니다.

양수 값을 갖는 수치 데이터와 함께 사용합니다. 

[box-cox-transformation 설명](https://www.statisticshowto.com/box-cox-transformation/)

[newton-raphson 공식](https://www.geeksforgeeks.org/program-for-newton-raphson-method/)

[위키 - 수식](https://en.wikipedia.org/wiki/Power_transform#Box–Cox_transformation)

## Implementation of Boxcox Transformation

[scipy 깃허브 링크](https://github.com/scipy)

#### Bloom filter Code block
{{< highlight text >}}
  
  # 1. scipy/stats/__init__.py

  stats 클래스에 메서드가 정의됨

  Transformations
  ===============
      
  .. autosummary::
    :toctree: generated/

    boxcox
    boxcox_normmax
    boxcox_llf
    yeojohnson

  # 2. scipy/special/functions.json

  Cython 으로 래핑되어있는 boxcox 함수임

      "boxcox": {
          "_boxcox.pxd": {
              "boxcox": "dd->d"
          }
      },
      "boxcox1p": {
          "_boxcox.pxd": {

  # 3. scipy/scipy/special/_boxcox.pxd
  
{{< /highlight >}}

Cython 으로 정의되어 있고, libc math api의 fabs, expm1 로 구현되어 있음.

1차원 배열의 값은 아래의 변환을 거침.
#### libc.math - fab

[fab](https://man7.org/linux/man-pages/man3/fabs.3.html)

fabs, fabsf, fabsl - absolute value of floating-point number

부동소수점 절대값임. 아래의 함수에서 보면 10^(-19) 보다 작을 경우 0으로 간주함.

#### libc.math - expm1

[expm1](https://man7.org/linux/man-pages/man3/expm1.3.html)

expm1, expm1f, expm1l - exponential minus 1

링크에서 보여준 공식 그대로 사용하는 것을 알 수 있음.

#### libc.math Cython package

역시 c 는 number cruncher 들을 위한 프로그래밍 언어다.

{{< highlight text >}}
  
  cdef inline double boxcox(double x, double lmbda) nogil:
      # if lmbda << 1 and log(x) < 1.0, the lmbda*log(x) product can lose
      # precision, furthermore, expm1(x) == x for x < eps.
      # For doubles, the range of log is -744.44 to +709.78, with eps being
      # the smallest value produced.  This range means that we will have
      # abs(lmbda)*log(x) < eps whenever abs(lmbda) <= eps/-log(min double)
      # which is ~2.98e-19.  
      if fabs(lmbda) < 1e-19:
          return log(x)
      else:
          return expm1(lmbda * log(x)) / lmbda          
      ....

{{< /highlight >}}


