+++
author = "Paran Lee"
title = "Chisel Overview"
date = "2021-03-01"
description = "새로운 HDL Chisel, and scala"
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

최근 Softcore 동향에 인기있는 Chisel 을 소개합니다.

*Constructing Hardware in a Scala Embedded Language (Chisel)*

Chisel 의 특성을 살펴보면

RTL generator 들은 Chisel 로 만들어집니다.
- scala 를 기반으로 사용하는 HDL

Scala 언어의 좋은 특성을 많이 쓸 수 있습니다.
- object-oriented programming
- functional programming 

또 흥미로운 프로젝트들이 많이 있는데, 하나를 예로 들면

RISC-V "Rocket Chip" SoC Generator[^1]

특히 Rocket Chip[^2] 을 기반으로 FPGA 보드에 올려서 만든 

lowrisc 데모영상을 보고 감동을 받았습니다.

#### lowrisc demo

<br>  

{{< youtube oKz-Yyun9NM >}}

<br>
  
그 감동의 원인은, 

기존 FPGA & Arm (기타 등등..) core 가 SoC 에 들어있어 리눅스 부팅 가능한 보드가 아니라

FPGA 에서 합성해서 CPU, FPU, 메모리 컨트롤러, 버스까지 개발자가 뚝딱!

그것도 펌웨어 수준이 아니라, 리눅스 부팅까지 가능한 하드웨어 설계라는 점입니다!

굉장히 범용적으로 하드웨어 가속화를 사용할 수 있을거라 생각이 드네요.

lowrisc getting started [^3]에 보면 위의 데모를 위한 내용이 나와있습니다.
  

## Chisel example source code

adder 코드 예시는 아래와 같습니다.

#### example - adder

{{< highlight scala >}}

class Add extends Module {

    val io = IO(new Bundle {
        val a = Input(UInt(8.W))
        val b = Input(UInt(8.W))
        val y = Output(UInt(8.W))
    })

    io.y := io.a + io.b
}

{{< /highlight >}}

최근에 나온 언어들의 특징이기도 하고,

Scala 문법을 따라서

모듈마다 명시해주던 변수 선언이 간편해졌네요.

#### example - stack 

{{< highlight scala >}}

class Stack(val depth: Int) extends Module {
    
    val io = new Bundle {
        val push = Bool(INPUT)
        val pop = Bool(INPUT)
        val en = Bool(INPUT)
        val dataIn = UInt(INPUT, 32)
        val dataOut = UInt(OUTPUT, 32)
    }

    val stack_mem = Mem(UInt(width = 32), depth)
    val sp = Reg(init = UInt(0, width = log2Up(depth+1)))
    val dataOut = Reg(init = UInt(0, width = 32))

    when (io.en) {
        when(io.push && (sp < UInt(depth))) {
            stack_mem(sp) := io.dataIn
            sp := sp + UInt(1)
        } .elsewhen(io.pop && (sp > UInt(0))) {
            sp := sp - UInt(1)
        }

        when (sp > UInt(0)) {
            dataOut := stack_mem(sp - UInt(1))
        }
    }

    io.dataOut := dataOut
}

{{< /highlight >}}

호출해서 사용하는 각 모듈이 어떤식으로 Overload 되어 있는지 궁금해지는 코드네요.

#### example - stack unit test

{{< highlight scala >}}

class StackTests(c: Stack) extends Tester(c) {
    var nxtDataOut = 0
    val stack = new ScalaStack[Int]()

    for (t <- 0 until 16) {
        val enable = rnd.nextInt(2)
        val push = rnd.nextInt(2)
        val pop = rnd.nextInt(2)
        val dataIn = rnd.nextInt(256)
        val dataOut = nxtDataOut

        if (enable == 1) {
            if (stack.length > 0)
                nxtDataOut = stack.top

            if (push == 1 && stack.length < c.depth) {
                stack.push(dataIn)
            } else if (pop == 1 && stack.length > 0) {
                stack.pop()
            }
        }

        poke(c.io.pop, pop)
        poke(c.io.push, push)
        poke(c.io.en, enable)
        poke(c.io.dataIn, dataIn)

        step(1)
        
        expect(c.io.dataOut, dataOut)
    }
}

{{< /highlight >}}

unit test 코드는 과연 이 코드가 하드웨어를 테스트 하는게 맞을까? 하는 생각이 드네요.

<br>
  
## Summary

오늘날 소프트웨어 개발이 블랙박스를 가지고 편하게 비지니스 로직을 개발하듯이,

하드웨어 개발도 얼마 만큼 편하고 생산성 좋게 구현할 수 있을지 기대되고 궁금하네요.

<br>

[^1]: Chisel – Accelerating Hardware Design pdf [link](https://riscv.org/wp-content/uploads/2015/01/riscv-chisel-tutorial-bootcamp-jan2015.pdf)
[^2]: Rocket Chip pdf [link](https://riscv.org/wp-content/uploads/2015/01/riscv-rocket-chip-generator-workshop-jan2015.pdf)
[^3]: lowrisc getting started [link](https://www.lowrisc.org/docs/getting-started/)
