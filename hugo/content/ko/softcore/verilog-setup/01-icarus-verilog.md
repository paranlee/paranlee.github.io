+++
author = "Paran Lee"
title = "Install - Icarus verilog"
date = "2021-03-03"
description = "Icarus verilog 설치하기"
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
series = ["Softcore"]
+++

## Overview

패키지 업데이트가 비교적 느린편이므로, 성능 & 기능이 우수한 최신 릴리즈를 사용하려고 합니다.

<!--more-->

#### Icarus verilog install
{{< highlight bash >}}
    $ sudo apt install autoconf gperf

    $ git clone https://github.com/steveicarus/iverilog.git

    ~/iverilog$ git tag

    ...

    v10_0
    v10_1
    v10_1_1
    v10_2
    v10_3

    ...

    $ git checkout v10_3
    $ sh autoconf.sh

    $ ./configure 
    $ make
    $ sudo make install
{{< /highlight >}}

[설치 관련해서 참고하면 좋은 문서](https://iverilog.fandom.com/wiki/Installation_Guide)

설치가 끝났으니 테스트 합니다~

#### helloverilog.v
{{< highlight verilog >}}

module helloverilog;
    initial
        $display("Hello, Verilog!");
endmodule

{{< /highlight >}}

iverilog 컴파일러를 실행시킵니다.

#### iverilog compile
{{< highlight bash >}}

$ iverilog hello.v -o hello

{{< /highlight >}}

시뮬레이션 합니다.

자세한 과정은 차차 알아나가보죠~

#### Run
{{< highlight bash >}}

$ vvp hello
Hello, Verilog!

{{< /highlight >}}

성공적으로 설치했습니다. 짝짝짝

