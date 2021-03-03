+++
author = "Paran Lee"
title = "linux kernel version"
date = "2021-03-01"
description = "Linux kernel version 그리고 (Super) Long Term Support"
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

리눅스 4.4 & 4.19 는 현재도 현역 커널로 활동중입니다.[^1]
이 두 버전은 SLTS (Super Long Term Support) 로 현재까지도 vanilla Linux kernel upstream 에서 유지보수하는 커널 버전이기 때문입니다.

해당 커널 버전은 송전, 정유, 가스 시설 등등... 우리 도시를 이루는 핵심 인프라에서 사용하기 때문이죠.

SLTS 에 해당하는 버전들을 [커널 소스 태그](https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/)에서나
[bootlin](https://elixir.bootlin.com/)에 들어가셔서 릴리즈 번호를 보면 아마 깜짝 놀라실 겁니다.

## 다음번 SLTS 는 언제 나오나요?

#### Debian 11

> Debian 11 for release, began on 13 January 2021.</p>
> — <cite>The Debian release team[^2]</cite>

#### CIP

> By starting the SLTS kernel development, CIP would be ready to align with a new Debian release which is expected in 2021.</p>
> — <cite>CIVIL INFRASTRUCTURE PLATFORM[^4]</cite>

## Debian release tables

CIP 에서 언급했듯이 데비안 11 에서 리눅스 커널 버전이 들어가 있는 것을 확인할 수 있습니다. [^3]

   Version (Code name) | Linux kernel | 
-----------------------|--------------|
         11 (Bullseye) |         5.10 |

[^1]: Linux kernel version history [talk](https://en.wikipedia.org/wiki/Linux_kernel_version_history)
[^2]: Debian 11 for release, began on 13 January 2021. [talk](https://www.phoronix.com/scan.php?page=news_item&px=Debian-11-Freeze-Starts)
[^3]: Debian 11 -- Release Notes [talk](https://www.debian.org/releases/testing/releasenotes)
[^4]: CIP would be ready to align with a new Debian release which is expected in 2021. [talk](https://www.cip-project.org/blog/2020/12/02/cip-to-embark-on-kernel-5-10-development-for-slts)

