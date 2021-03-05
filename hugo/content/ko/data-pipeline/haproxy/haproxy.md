+++
author = "Paran Lee"
title = "HA Proxy sticky session"
date = "2021-03-01"
description = "HA Proxy sticky session 간단한 정리"
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
series = ["Themes Guide"]
+++

<!--more-->

## HA Proxy?

L4 의 TCP (UDP 는 지원안함), L7의 HTTP 라우팅 기능을 하는 오픈소스 HA(High Availability) Proxy 서버임

프록시하는 노드들을 Heartbeat 로 Health 체크함 

장애가 있는 서비스는 제외하고, 대응하는 여분의 Stanby 서비스가 있으면 이쪽으로 라우팅해줌

L4 레이어 단계의 Log 기능이 있음

Shared frontend 로 HA Proxy 노드도 고가용성을 가지면서 확장 가능함

## IP로 세션 유지하기

Client IP에 대한 해쉬 테이블을 만들어서 찰싹 붙임

####  /etc/haproxy/haproxy.cfg

	# ...
	
	# round robin balancing between the various backeands
	backend app
	    balance roundrobin
	    
	    # 클라이언트 별 IP 값으로 sticky session
	    hash-type consistent
	    
	    server tcpserver01 192.168.10.1:30001 S01 check
	    server tcpserver01 192.168.10.2:30002 S02 check
	    # server app1 192.168.10.1:30001 check
	    # server app2 192.168.10.2:30002 check
	
	# ...
