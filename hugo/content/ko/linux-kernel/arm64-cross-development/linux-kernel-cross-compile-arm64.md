+++
author = "Paran Lee"
title = "QEMU x86_64 machine full virtualized arm64 linux deveolpmet enviroment"
date = "2021-03-04"
description = "QEMU 전가상화로 x86_64 리눅스에서 arm64 개발 & 테스트 환경 구성하기"
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

QEMU 전가상화로 x86_64 리눅스 머신에서 arm64 개발 & 테스트 환경을 구성해봅니다.

qemu-arm-aarch64 와 라즈베리파이4 머신 세팅 기반, 

aarch64 데비안 배포판 이미지 기반으로 네트워크 설정을 하고

전가상화 개발 & 테스트 환경을 구축합니다.

<!--more-->

## 가상화 환경 구축 - full virtualized environment

[데비안 라즈베리 파이 다운로드 페이지](https://raspi.debian.net/tested-images/)에서 원하는 이미지를 다운로드 받습니다.

[Debian 11 버전 라즈베리파이4](https://raspi.debian.net/daily/raspi_4_bullseye.img.xz) 를 다운로드 받았습니다.

라즈베리파이 4 이미지를 다운로드 받고 압축을 해제해줍니다.

#### raspi_4_bullseye.img.xz
{{< highlight bash >}}

~$ mkdir rpi4_qemu

~/rpi4_qemu$ wget https://raspi.debian.net/daily/raspi_4_bullseye.img.xz
--2021-03-04 11:08:19--  https://raspi.debian.net/daily/raspi_4_bullseye.img.xz
Resolving raspi.debian.net (raspi.debian.net)... 208.97.148.173, 194.58.198.32, 64.68.197.10, ...
Connecting to raspi.debian.net (raspi.debian.net)|208.97.148.173|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 371554080 (354M) [application/x-xz]
Saving to: ‘raspi_4_bullseye.img.xz’

raspi_4_bullseye.img.xz       100%[=================================================>] 354.34M  2.52MB/s    in 2m 21s

2021-03-04 11:10:42 (2.51 MB/s) - ‘raspi_4_bullseye.img.xz’ saved [371554080/371554080]

~/rpi4_qemu$ ls raspi_4_bullseye.img.xz
raspi_4_bullseye.img.xz
~/rpi4_qemu$ xz --decompress raspi_4_bullseye.img.xz

{{< /highlight >}}

이미지를 부팅하기 위해서 파티션을 만들고, 마운트합니다.

#### raspi_4_bullseye.img mount
{{< highlight bash >}}

#  we need to determine the file byte 
# offset for the first partition in order to mount it.

~/rpi4_qemu$ sudo fdisk -l raspi_4_bullseye.img

Disk raspi_4_bullseye.img: 1.48 GiB, 1572864000 bytes, 3072000 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xe0444a45

Device                Boot  Start     End Sectors  Size Id Type
raspi_4_bullseye.img1        2048  614399  612352  299M  c W95 FAT32 (LBA)
raspi_4_bullseye.img2      614400 3071999 2457600  1.2G 83 Linux

~/rpi4_qemu$ mkdir -p mnt/rpi4

# Use the start sector (2048) of the first partition 
# and multiply it with the sector size (512). 2048*512=1048576

# Use this number to mount with offset the first partition:

~/rpi4_qemu$ sudo mount -o offset=1048576 raspi_4_bullseye.img mnt/rpi4

~/rpi4_qemu$ ls mnt/rpi4/
bcm2711-rpi-4-b.dtb       bootcode.bin  fixup4cd.dat  fixup_x.dat                start4db.elf  sysconf.txt
bcm2837-rpi-3-a-plus.dtb  cmdline.txt   fixup4db.dat  initrd.img-5.10.0-3-arm64  start4x.elf   vmlinuz-5.10.0-3-arm64
bcm2837-rpi-3-b-plus.dtb  config.txt    fixup4x.dat   start.elf                  start_cd.elf
bcm2837-rpi-3-b.dtb       fixup.dat     fixup_cd.dat  start4.elf                 start_db.elf
bcm2837-rpi-cm3-io3.dtb   fixup4.dat    fixup_db.dat  start4cd.elf               start_x.elf

~/rpi4_qemu$ cp mnt/rpi4/vmlinuz-5.10.0-3-arm64 .
~/rpi4_qemu$ cp mnt/rpi4/initrd.img-5.10.0-3-arm64 .

~/rpi4_qemu$ ls
initrd.img-5.10.0-3-arm64  mnt  raspi_4_bullseye.img  vmlinuz-5.10.0-3-arm64

~/rpi4_qemu$ qemu-system-aarch64 --help
QEMU emulator version 4.2.1 (Debian 1:4.2-3ubuntu6.14)

{{< /highlight >}}

마운트한 이미지를 qemu-system-aarch64 를 사용해서 실행합니다.

메모리 옵션과 smp는 각자 환경에 맞춰 수정하면 됩니다.

#### qemu-system-aarch64
{{< highlight bash >}}

qemu-system-aarch64 -M virt -m 8192 -smp 8 -cpu cortex-a72 \
-kernel vmlinuz-5.10.0-3-arm64 \
-initrd initrd.img-5.10.0-3-arm64 \
-drive if=none,file=raspi_4_bullseye.img,format=raw,id=hd \
-append 'root=/dev/vda2 noresume' \
-device virtio-blk-pci,drive=hd \
-device virtio-net-pci,netdev=mynet \
-netdev user,id=mynet,hostfwd=tcp::2222-:22 \
-device virtio-rng-pci -no-reboot -nographic \
-net nic -net tap,ifname=tap1,script=no -net socket,listen=localhost:8080

{{< /highlight >}}

root 계정으로 로그인하면되고, 별도의 패스워드는 없습니다.

전가상화 환경의 세팅은 아래의 링크를 참고하면 좋습니다.

[라즈베리파이3 가상화 환경에서 베어메탈 프로그래밍](https://raspberrypi.stackexchange.com/questions/34733/how-to-do-qemu-emulation-for-bare-metal-raspberry-pi-images)

[라즈베리파이3 가상화 환경으로 리눅스 데비안 배포판 올리기](https://wiki.arcoslab.org/doku.php?id=tutorials:debian_buster_for_rpi3_with_qemu)

[라즈베리파이 모델별 데비안 이미지 다운로드](https://wiki.debian.org/RaspberryPiImages)


## 네트워크 설정하기 - full virtualized network setup

이제 전가상화 환경에서 네트워크를 이용하여 배포판 패키지를 이용할 수 있도록

TUN/TAP 으로 이더넷 하드웨어 전가상화를 설정하겠습니다.

일단 QEMU 호스트에서 설정을 진행합니다.

#### Inbound - Host

{{< highlight bash >}}

## HOST (WSL2)

# openVPN의 TAP 가상 이더넷 디바이스를 추가함
$ sudo apt -y install openvpn

$ sudo openvpn --mktun --dev tap1
Thu Mar  4 11:46:28 2021 TUN/TAP device tap1 opened
Thu Mar  4 11:46:28 2021 Persist state set to: ON

$ ip addr show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: bond0: <BROADCAST,MULTICAST,MASTER> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 4e:9d:59:d1:d3:cd brd ff:ff:ff:ff:ff:ff
3: dummy0: <BROADCAST,NOARP> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 42:70:8b:56:3e:06 brd ff:ff:ff:ff:ff:ff
4: sit0@NONE: <NOARP> mtu 1480 qdisc noop state DOWN group default qlen 1000
    link/sit 0.0.0.0 brd 0.0.0.0
5: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:15:5d:be:13:e7 brd ff:ff:ff:ff:ff:ff
    inet 172.25.229.250/20 brd 172.25.239.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::215:5dff:febe:13e7/64 scope link
       valid_lft forever preferred_lft forever
6: tap1: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 100
    link/ether 8e:1a:cb:7e:99:71 brd ff:ff:ff:ff:ff:ff

$ sudo ifconfig tap1 192.168.105.1 up
$ ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.21.36.142  netmask 255.255.240.0  broadcast 172.21.47.255
        inet6 fe80::215:5dff:fe98:245a  prefixlen 64  scopeid 0x20<link>
        ether 00:15:5d:98:24:5a  txqueuelen 1000  (Ethernet)
        RX packets 342  bytes 35884 (35.8 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 19  bytes 1514 (1.5 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

tap1: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        inet 192.168.105.1  netmask 255.255.255.0  broadcast 192.168.105.255
        ether e6:9e:44:f3:25:57  txqueuelen 100  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

# DNS 설정부분 (배포판 패키지를 설치하기 위해서는 DNS 설정이 꼭 필요함)
$ cat /etc/resolv.conf
# This file was automatically generated by WSL. To stop automatic generation of this file, add the following entry to /etc/wsl.conf:
# [network]
# generateResolvConf = false
nameserver 8.8.8.8

{{< /highlight >}}

게스트에서 고정 IP 및 포워드 게이트웨이를 설정하고

DNS 설정을 추가해주어야 합니다.

#### Inbound - Guest
{{< highlight bash >}}

## GUEST (QEMU in a WSL2)

root@rpi4-20210303:~# cat /etc/network/interfaces
auto enp0s1
iface enp0s1 inet static
    address 192.168.105.2
    netmask 255.255.255.0
    gateway 192.168.105.1
    dns-nameserver 172.21.32.1
    
root@rpi4-20210303:~# /etc/init.d/networking restart
root@rpi4-20210303:~# hostname -I
192.168.105.2

root@rpi4-20210303:~# cat /etc/resolvconf/resolv.conf.d/tail
nameserver 8.8.8.8

$ /etc/init.d/networking restart

root@rpi4-20210303:~# ping 172.21.36.142
PING 172.21.36.142 (172.21.36.142) 56(84) bytes of data.
64 bytes from 172.21.36.142: icmp_seq=1 ttl=64 time=0.571 ms
64 bytes from 172.21.36.142: icmp_seq=2 ttl=64 time=0.404 ms
64 bytes from 172.21.36.142: icmp_seq=3 ttl=64 time=0.373 ms
^C
--- 172.21.36.142 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2004ms
rtt min/avg/max/mdev = 0.373/0.449/0.571/0.086 ms

{{< /highlight >}}

여기까지 인바운드 설정은 완료했고, HOST 와 연결된 것을 확인할 수 있습니다.

마지막으로 작업으로 게스트가 호스트를 통해서 외부망과 소통할 수 있도록

NAT 아웃바운드 설정을 해야합니다. 

다시 호스트를 볼까요?

#### Outbound - Host
{{< highlight bash >}}
## HOST (WSL2)

$ hostname -I
172.21.36.142 192.168.105.1

$ sudo sysctl -w net.ipv4.ip_forward=1
net.ipv4.ip_forward = 1
$ ping 192.168.105.2
PING 192.168.105.2 (192.168.105.2) 56(84) bytes of data.
64 bytes from 192.168.105.2: icmp_seq=1 ttl=64 time=0.807 ms
64 bytes from 192.168.105.2: icmp_seq=2 ttl=64 time=1.38 ms
^C
--- 192.168.105.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1019ms
rtt min/avg/max/mdev = 0.807/1.093/1.380/0.286 ms

$ sudo iptables -t nat -A POSTROUTING -s 192.168.105.0/24 -o eth0 -j SNAT --to 172.21.36.142

{{< /highlight >}}

자 이제 게스트 머신에서 패키지 업데이트를 진행해보겠습니다.

#### Outbound - Guest
{{< highlight bash >}}

## GUEST (QEMU in a WSL2)

root@rpi4-20210303:~# ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=113 time=36.4 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=113 time=37.5 ms
^C
--- 8.8.8.8 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1003ms
rtt min/avg/max/mdev = 36.388/36.944/37.501/0.556 ms

root@rpi4-20210303:~# apt -y update && apt -y upgrade
Hit:1 http://deb.debian.org/debian bullseye InRelease
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
All packages are up to date.
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Calculating upgrade... Done
0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.

{{< /highlight >}}

여기까지 설정하는데 수고많으셨습니다.

그런데, 데비안 이미지의 기본 파티션의 사이즈가 작아서 패키지를 설치하는데 문제가 있습니다.

그리고 막상 패키지를 설치할 수 있게되었는데, 

파티션 용량이 1.2 GB 정도로 굉장히 작아서 이를 늘려줄 필요가 있습니다.


## 파티션 사이즈 조정 - Increase partition size

fdisk 와 resize2fs 를 이용해서 파티션 사이즈를 늘려줍니다.

#### fdisk & resize2fs
{{< highlight bash >}}

## GUEST (QEMU in a WSL2)

root@rpi4-20210303:~# fdisk -l
Disk /dev/vda: 21.46 GiB, 23047700480 bytes, 45015040 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xe0444a45

Device     Boot  Start     End Sectors  Size Id Type
/dev/vda1         2048  614399  612352  299M  c W95 FAT32 (LBA)
/dev/vda2       614400 3071999 2457600  1.2G 83 Linux
root@rpi4-20210303:~# lsblk
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
vda    254:0    0 21.5G  0 disk
├─vda1 254:1    0  299M  0 part /boot/firmware
└─vda2 254:2    0  1.2G  0 part /
root@rpi4-20210303:~# df -h
Filesystem      Size  Used Avail Use% Mounted on
udev            3.9G     0  3.9G   0% /dev
tmpfs           795M  348K  795M   1% /run
/dev/vda2       1.2G  969M  101M  91% /
tmpfs           3.9G     0  3.9G   0% /dev/shm
tmpfs           5.0M     0  5.0M   0% /run/lock
/dev/vda1       299M   73M  227M  25% /boot/firmware
tmpfs           795M     0  795M   0% /run/user/0
root@rpi4-20210303:~# fdisk /dev/vda

Welcome to fdisk (util-linux 2.36.1).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.


Command (m for help): u
Changing display/entry units to cylinders (DEPRECATED!).

Command (m for help): p
Disk /dev/vda: 21.46 GiB, 23047700480 bytes, 45015040 sectors
Geometry: 4 heads, 32 sectors/track, 44657 cylinders
Units: cylinders of 128 * 512 = 65536 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xe0444a45

Device     Boot Start   End Cylinders  Size Id Type
/dev/vda1          17  4800      4785  299M  c W95 FAT32 (LBA)
/dev/vda2        4801 24000     19201  1.2G 83 Linux

Command (m for help): a
Partition number (1,2, default 2): 1

The bootable flag on partition 1 is enabled now.

Command (m for help): a
Partition number (1,2, default 2): 2

The bootable flag on partition 2 is enabled now.

Command (m for help): d
Partition number (1,2, default 2): 2

Partition 2 has been deleted.

Command (m for help): n
Partition type
   p   primary (1 primary, 0 extended, 3 free)
   e   extended (container for logical partitions)
Select (default p): p
Partition number (2-4, default 2): 2
First cylinder (4801-44657, default 4801):
Last cylinder, +/-cylinders or +/-size{K,M,G,T,P} (4801-44657, default 44657):

Created a new partition 2 of type 'Linux' and of size 2.4 GiB.
Partition #2 contains a ext4 signature.

Do you want to remove the signature? [Y]es/[N]o: n

Command (m for help): p

Disk /dev/vda: 21.46 GiB, 23047700480 bytes, 45015040 sectors
Geometry: 4 heads, 32 sectors/track, 44657 cylinders
Units: cylinders of 128 * 512 = 65536 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xe0444a45

Device     Boot Start   End Cylinders  Size Id Type
/dev/vda1  *       17  4800      4785  299M  c W95 FAT32 (LBA)
/dev/vda2        4801 44657     39858  2.4G 83 Linux

Command (m for help): a
Partition number (1,2, default 2): 1

The bootable flag on partition 1 is disabled now.

Command (m for help): w
The partition table has been altered.
Syncing disks.

root@rpi4-20210303:~# reboot

# 새로 잡힌 파티션에서 resize2fs 적용하기

df root@rpi4-20210303:~# df -h
Filesystem      Size  Used Avail Use% Mounted on
udev            3.9G     0  3.9G   0% /dev
tmpfs           795M  352K  795M   1% /run
/dev/vda2       1.2G  970M  101M  91% /
tmpfs           3.9G     0  3.9G   0% /dev/shm
tmpfs           5.0M     0  5.0M   0% /run/lock
/dev/vda1       299M   73M  227M  25% /boot/firmware
tmpfs           795M     0  795M   0% /run/user/0
root@rpi4-20210303:~# lsblk
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
vda    254:0    0 21.5G  0 disk
├─vda1 254:1    0  299M  0 part /boot/firmware
└─vda2 254:2    0  2.4G  0 part /

root@rpi4-20210303:~# resize2fs /dev/vda2
resize2fs 1.46.1 (9-Feb-2021)
Filesystem at /dev/vda2 is mounted on /; on-line resizing required
old_desc_blocks = 1, new_desc_blocks = 1
[   59.397302] EXT4-fs (vda2): resizing filesystem from 307200 to 637712 blocks
[   59.414158] EXT4-fs (vda2): resized filesystem to 637712
The filesystem on /dev/vda2 is now 637712 (4k) blocks long.

root@rpi4-20210303:~# df -h
Filesystem      Size  Used Avail Use% Mounted on
udev            3.9G     0  3.9G   0% /dev
tmpfs           795M  348K  795M   1% /run
/dev/vda2       2.4G  981M  1.3G  43% /
tmpfs           3.9G     0  3.9G   0% /dev/shm
tmpfs           5.0M     0  5.0M   0% /run/lock
/dev/vda1       299M   73M  227M  25% /boot/firmware
tmpfs           795M     0  795M   0% /run/user/0


{{< /highlight >}}

디스크 사이즈를 충분히 늘려놓은 것을 확인했습니다.

이상, 전가상화 환경에서 즐거운 개발하세요~

