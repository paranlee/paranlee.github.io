+++
author = "Paran Lee"
title = "Install - GTK wave"
date = "2021-03-03"
description = "GTK wave 설치하기"
weight = 3
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

디지털회로 디버깅을 위해서 value change dump 파일로 클록, 입출력 등을 보여주는 GTK Wave 를 설치합니다. 

이 패키지는 최신 릴리즈가 성능에는 큰 영향이 없다고 생각이 들어서 그냥 패키지 매니저로 설치했습니다.

<!--more-->

#### Install gtkwave on ubuntu
{{< highlight verilog >}}

$ sudo apt -y install gtkwave

{{< /highlight >}}

테스트 파일을 작성해봅니다.

#### trace.v
{{< highlight bash >}}

/*
 * 4bit_unssigned_adder & bit detector
 *
 * output : 
 * @clk : internal clock
 * @a : 
 * @b
 * 
 */

module trace;
    
    reg clk = 0;
    reg[3:0] a = 4'd0;
    reg b = 0;
    
    always #1 clk = ~clk;
    
    always @(posedge clk) begin
        a = a + 1;
        b = a[2];
    end
    
    initial begin
        $dumpfile("trace.vcd");
        $dumpvars(0, trace); // all vars dump
        #100 $finish; // 100 second end time
    end 
    
endmodule

{{< /highlight >}}

$finish 부분은 종료되는 시점을 정합니다.

해당 구문이 없으면 시뮬레이션이 계속 진행 되버립니다.

#### setup.sh
{{< highlight bash >}}

$ iverilog trace.v -o trace

$ vvp trace
VCD info: dumpfile trace.vcd opened for output.

{{< /highlight >}}

만들어진 trace.vcd 파일 gtkwave 에서 실행합니다.

#### trace.v 를 시뮬레이션한 결과를 GTKWave 로 확인하기

<p></p>

<img src= "/images/softcore/gtk-wave.png">

<p></p>

dumpvars 에서 모든 변수를 덤프하므로, 

SST 에 모듈을 선택하고, 덤프한 signal 들의 파형을 조회할 수 있게 signal 메뉴로 드래그 드롭합니다.

그리고 메뉴 항목에서 Time →Zoom → Zoom In 으로 확대할 수 있습니다.

