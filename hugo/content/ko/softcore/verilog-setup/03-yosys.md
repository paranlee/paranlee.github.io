+++
author = "Paran Lee"
title = "Install - Yosys"
date = "2021-03-03"
description = "Yosys 설치하기"
weight = 4
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
series = ["Linux kernel"]
+++

## Yosys 설치하기

yosys 는 베릴로그 RTL 합성 툴입니다. 

결과는 게이트를 합성하고 실제 칩의 하드웨어 도면을 볼 수 있습니다.

yosys 도 기능과 성능이 우수한 최신 릴리즈로 설치합니다.

(yosys github)[https://github.com/YosysHQ/yosys] setup 항목을 참고하시면 좋습니다.

#### Install dependency on ubuntu
{{< highlight bash >}}

$ sudo apt install build-essential clang bison flex \
	libreadline-dev gawk tcl-dev libffi-dev git \
	graphviz xdot pkg-config python3 libboost-system-dev \
	libboost-python-dev libboost-filesystem-dev zlib1g-dev

# 위의 패키지 말고도 추가적으로 설치했던 패키지
$ sudo apt install tcl8.6-dev gawk

$ git clone https://github.com/YosysHQ/yosys
# == git clone https://github.com/cliffordwolf/yosys.git

~/yosys$ git tag
yosys-0.2.0
yosys-0.3.0
yosys-0.4
yosys-0.5
yosys-0.6
yosys-0.7
yosys-0.8
yosys-0.9

git checkout yosys-0.9
sudo make install

{{< /highlight >}}

