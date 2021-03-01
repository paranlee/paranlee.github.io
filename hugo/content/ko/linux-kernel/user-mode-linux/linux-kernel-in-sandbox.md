+++
author = "Hugo Authors"
title = "Linux kernel in sandbox"
date = "2021-03-01"
description = "응용프로그램처럼 마음대로 뽀개기"
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

리눅스 커널 소스를 클론하고, 응용프로그램 다루듯이 마음껏 뽀개도록,

User mode linux 라는 feature 를 사용하려고 합니다.

<!--more-->

## User mode Linux

리눅스 커널 소스 코드를 클론합니다.

버전 선택은 마음대로 하시면 됩니다.

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

빌드할 때 특별히 설정 해주는 플래그입니다.

#### Setup build flags
{{< highlight bash >}}

# arch setup & debug symbol
export CFLAGS="-g -Wall -Wextra"
export ARCH=um 
export SUBARCH=x86_64

{{< /highlight >}}

이제 빌드를 해봅시다.

#### config & compile
{{< highlight bash >}}

# make default config
make defconfig

# make user mode linux
make -j8 linux

{{< /highlight >}}

루트 파일시스템을 마운트 합니다.
저는 보통 소스 디렉토리에 해놓습니다.

#### root file system mount
{{< highlight bash >}}
sudo apt -y install supermin

supermin -v --prepare bash coreutils -o $PWD/rootfs.template
supermin -v --build --format chroot rootfs.template -o $PWD/rootfs
{{< /highlight >}}

마지막으로 마운트한 경로에 스크립트를 작성하고, 

#### rootfs/boot/boot.sh
{{< highlight bash >}}
#!/bin/bash
mount -t sysfs /sys /sys
mount -t proc /proc /proc
exec /bin/bash
{{< /highlight >}}

실행권한을 변경하면 지루한 설정은 끝났습니다!

#### chmod
{{< highlight bash >}}
chmod +x rootfs/boot/boot.sh
{{< /highlight >}}

자 이제 user mode linux 를 실행하고 즐겨봅니다.

#### Have a lot of fun
{{< highlight bash >}}
./linux rootfstype=hostfs rootflags=$PWD/rootfs rw init=/boot/boot.sh
{{< /highlight >}}

다음에는 커널 소스를 Hack 한 다음 GDB TUI 모드에서 디버깅하는 과정을 살펴봅니다.

