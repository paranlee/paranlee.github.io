+++
author = "Paran Lee"
title = "Linux kernel {x86_64, arm64} in the sandbox"
date = "2021-03-01"
description = "응용프로그램처럼 마음대로 커널 뽀개기"
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

빌드할 때 특별히 설정 해주는 플래그입니다.

#### Setup build flags
{{< highlight bash >}}

# arch setup & debug symbol
export CFLAGS="-g -Wall -Wextra"
export ARCH=um 
export SUBARCH=x86_64 # export SUBARCH=arm64

{{< /highlight >}}

이제 빌드를 해봅시다.

#### config & compile 1
{{< highlight bash >}}

# make default config
make defconfig

{{< /highlight >}}

여기서 잠깐, 우리는 열심히 리눅스 커널을 해킹할것이므로

아래의 추가 설정을 해줍시다!

DDD나 Insight를 사용해서 디버깅하는 것도 가능합니다.
커널을 직접 빌드하는 경우에 디버깅이 가능하게 하려면 다음 옵션을 선택하면 됩니다.

    Kernel Hacking
        ->Compile the kernel with frame pointers - Enable
        ->Show command line arguments on the host in TT mode - Disable

#### config & compile +α
{{< highlight bash >}}

# make default config
 sudo apt install -y libncurses-dev

 make menuconfig

 .config - Linux/x86 5.10.18 Kernel Configuration
 ─────────────────────────────────────────────────────────────────────────────────
  ┌────────────────── Linux/x86 5.10.18 Kernel Configuration ──────────────────┐
  │  Arrow keys navigate the menu.  <Enter> selects submenus ---> (or empty    │
  │  submenus ----).  Highlighted letters are hotkeys.  Pressing <Y> includes, │
  │  <N> excludes, <M> modularizes features.  Press <Esc><Esc> to exit, <?>    │
  │  for Help, </> for Search.  Legend: [*] built-in  [ ] excluded  <M> module │
  │ ┌────────────────────────────────────────────────────────────────────────┐ │
  │ │        General setup  --->                                             │ │
  │ │    [*] 64-bit kernel                                                   │ │
  │ │        Processor type and features  --->                               │ │
  │ │        Power management and ACPI options  --->                         │ │
  │ │        Bus options (PCI etc.)  --->                                    │ │
  │ │        Binary Emulations  --->                                         │ │
  │ │        Firmware Drivers  --->                                          │ │
  │ │    [*] Virtualization (NEW)  --->                                      │ │
  │ │        General architecture-dependent options  --->                    │ │
  │ │    [*] Enable loadable module support  --->                            │ │
  │ │    -*- Enable the block layer  --->                                    │ │
  │ │        IO Schedulers  --->                                             │ │
  │ │        Executable file formats  --->                                   │ │
  │ │        Memory Management options  --->                                 │ │
  │ │    [*] Networking support  --->                                        │ │
  │ │        Device Drivers  --->                                            │ │
  │ │        File systems  --->                                              │ │
  │ │        Security options  --->                                          │ │
  │ │    -*- Cryptographic API  --->                                         │ │
  │ │        Library routines  --->                                          │ │
  │ │        Kernel hacking  --->                                            │ │
  │ │                                                                        │ │
  │ └────────────────────────────────────────────────────────────────────────┘ │
  ├────────────────────────────────────────────────────────────────────────────┤
  │          <Select>    < Exit >    < Help >    < Save >    < Load >          │
  └────────────────────────────────────────────────────────────────────────────┘

 # 아래의 항목들 중 해킹을 위해서 필요한 항목을 선택하자 
 # TODO: 각 항목이 어떤 기능을 하는지 구체적으로 조사가 필요함

  │ ┌────────────────────────────────────────────────────────────────────────┐ │
  │ │        printk and dmesg options  --->                                  │ │
  │ │        Compile-time checks and compiler options  --->                  │ │
  │ │        Generic Kernel Debugging Instruments  --->                      │ │
  │ │    [*] Kernel debugging                                                │ │
  │ │    [*]   Miscellaneous debug code                                      │ │
  │ │        Memory Debugging  --->                                          │ │
  │ │    [ ] Debug shared IRQ handlers                                       │ │
  │ │        Debug Oops, Lockups and Hangs  --->                             │ │
  │ │        Scheduler Debugging  --->                                       │ │
  │ │    [ ] Enable extra timekeeping sanity checking                        │ │
  │ │        Lock Debugging (spinlocks, mutexes, etc...)  --->               │ │
  │ │    -*- Stack backtrace support                                         │ │
  │ │    [ ] Warn for all uses of unseeded randomness                        │ │
  │ │    [ ] kobject debugging                                               │ │
  │ │        Debug kernel data structures  --->                              │ │
  │ │    [ ] Debug credential management                                     │ │
  │ │        RCU Debugging  --->                                             │ │
  │ │    [ ] Force round-robin CPU selection for unbound work items          │ │
  │ │    [ ] Force extended block device numbers and spread them             │ │
  │ │    [ ] Latency measuring infrastructure                                │ │
  │ │    [*] Tracers  --->                                                   │ │
  │ │    [ ] Sample kernel code  ----                                        │ │
  │ │    [*] Filter access to /dev/mem (NEW)                                 │ │
  │ │    [ ]   Filter I/O access to /dev/mem (NEW)                           │ │
  │ │        x86 Debugging  --->                                             │ │
  │ │        Kernel Testing and Coverage  --->                               │ │
  │ └────────────────────────────────────────────────────────────────────────┘ │
{{< /highlight >}}


#### config & compile 2
{{< highlight bash >}}

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

