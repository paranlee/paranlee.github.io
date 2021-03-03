+++
author = "Paran Lee"
title = "Install - NetlistSVG"
date = "2021-03-03"
description = "NetlistSVG 설치하기"
weight = 5
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

## NetlistSVG 설치하기

베릴로그 코드를 바탕으로 손쉽게 이미지를 만들수 있는 NPM 패키지의 NetlistSVG를 설치합니다.

node.js & npm & npm 패키지에서 netlistsvg 설치가 필요합니다.

Node.js 공식 홈페이지에서 바이너리 파일을 받아도 되고, 빌드해도 됩니다.

깃허브 레포지토에 netlistsvg 를 실행해볼 수 있는 예제가 있습니다.

#### netlistsvg install

{{< highlight bash >}}

$ git clone https://github.com/nturley/netlistsvg
$ cd examples

{{< /highlight >}}

examples 디렉토리 아래에 있는 D flip-flop 예제로 svg 이미지 파일을 만들어보겠습니다.

예제의 모듈 이름을 DFF에서 dff 소문자로 수정했습니다.

#### dff.v

{{< highlight verilog >}}
// module DFF (output reg Q, input C, D, R);
module dff (
	input C, D, R, 
    output reg Q
);

	always @(posedge C)
		if (~R) begin
			Q <= 1'b0;
		end else begin
			Q <= D;
		end

endmodule
{{< /highlight >}}

클럭 C 가 rising edge 일때 동작하고,

리셋 입력 R 이 negative 신호가 들어오면 출력 Q 를 0으로 리셋합니다.

리셋 입력이 없을 경우, 출력 Q 는 입력 D 값을 저장하고, 변경이 없으면 클럭과 상관없이 해당 값을 출력합니다.

#### draw

<p></p>

<img src = "/images/softcore/dff.svg">

<p></p>

{{< highlight bash >}}

$ yosys -q -p "prep -top dff  write_json dff.json" dff.v
$ netlistsvg dff.json -o dff.svg

{{< /highlight >}}

