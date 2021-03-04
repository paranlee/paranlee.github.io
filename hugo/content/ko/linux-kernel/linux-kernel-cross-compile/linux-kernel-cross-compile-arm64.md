+++
author = "Paran Lee"
title = "Linux kernel cross compile arm64 on x86_64 machine"
date = "2021-03-03"
description = "이 글 보고 크로스 컴파일 빨리 해보자~"
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

## Overview

x86_64 머신에서 arm64 리눅스 커널을 빌드합니다.

<!--more-->

## User mode Linux

리눅스 커널 소스 코드를 클론합니다.

버전 선택은 마음대로 하시면 됩니다.

저는 LTS 또는 SLTS 를 더 선호합니다.

Github 레포지토리가 아니라

kernel.org Git 에서 클론하는 이유는 마이너 릴리즈에 대한 커밋도 들어가기 때문에,

해당 릴리즈에 최신 변경 사항을 확인할 수 있습니다.

#### Linux kernel source clone
{{< highlight bash >}}

git clone git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git

# 5.10.x latest (SLTS)
git tag | grep "5.10."
git checkout 5.10.19

{{< /highlight >}}


#### Ubuntu
{{< highlight bash >}}

# arch setup & debug symbol
sudo apt -y install gcc-aarch64-linux-gnu cscope libssl-dev \
autoconf automake autotools-dev curl libmpc-dev libmpfr-dev \
libgmp-dev gawk build-essential bison flex texinfo \
gperf libtool patchutils bc zlib1g-dev libexpat-dev

{{< /highlight >}}


최신 버전의  arm64 크로스 컴파일러를 받고 싶으시면 

[aarch64-linux-gnu-gcc](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-a/downloads) 링크에서 받을 수 있습니다.

arm64 에 맞춰서 빌드 플래그를 설정합니다.

#### setup.sh
{{< highlight bash >}}

cat > setup.sh

export ARCH=arm64
# export CROSS_COMPILE=입맛대로..
export CROSS_COMPILE=aarch64-linux-gnu-

# ctrl + d

source setup.sh

{{< /highlight >}}

그럼 이제 빌드를 합니다.

#### make
{{< highlight bash >}}

# defulat configuration file create
make defconfig

make -j8

# source tagging
make -j8 cscope tags

{{< /highlight >}}

이제 arm64 커널 소스 분석을 할 준비가 완료되었습니다.

