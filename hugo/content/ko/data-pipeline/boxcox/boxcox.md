+++
author = "Paran Lee"
title = "Boxcox transformation, why?"
date = "2021-03-01"
description = "boxcox transformation?"
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

## Boxcox transformation, why? perspective of workflow

차분 변환 (sort 후 뒤에 친구 값이랑 나랑 차이만 쏙)

→ boxcox transformation (복잡한 지수함수의 승수의 해를 뉴턴 메서드로 구하고 이를 정규분포로 변환)

→ 정규분포 (적당한 값 추리기 좋다)

→ 6 σ

→ 평범한 놈들 그래 니들을 원했어 ㅇㅇ

## Boxcox inner implementation

참고 [scipy](https://github.com/scipy)

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

### Box Cox 함수의 정의

[box-cox-transformation 설명](https://www.statisticshowto.com/box-cox-transformation/)

[위키 수식](https://en.wikipedia.org/wiki/Power_transform#Box–Cox_transformation)

### libc/math 함수에서의 fab & expm1

{{< highlight text >}}
  
[fab](https://man7.org/linux/man-pages/man3/fabs.3.html)

fabs, fabsf, fabsl - absolute value of floating-point number

{{< /highlight >}}

부동소수점 절대값임. 아래의 함수에서 보면 10^(-19) 보다 작을 경우 0으로 간주함.

{{< highlight text >}}
  
[expm1](https://man7.org/linux/man-pages/man3/expm1.3.html)

expm1, expm1f, expm1l - exponential minus 1

{{< /highlight >}}

링크에서 보여준 공식 그대로 사용하는 것을 알 수 있음.


### libc.math

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


