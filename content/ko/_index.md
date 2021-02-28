---
title: Paran Lee github.io
description: Hugo zzo, zdoc theme documentation home page
date: 2020-01-26T04:15:05+09:00
draft: false
# updatesBanner: "Banner - &nbsp; [Hugo ZDoc theme](https://github.com/zzossig/hugo-theme-zdoc) &nbsp; just arrived"
landing:
  height: 500
  image: favicon/android-icon-192x192.png
  title:
    - Document Blog
  text:
    - Paran Lee's research note
  titleColor:
  textColor:
  spaceBetweenTitleText: 25
  # buttons:
  #   - link: docs
  #     text: Docs
  #     color: primary
  # backgroundImage: 
  #   src: images/landscape.jpg
  #   height: 600

sections:
  - bgcolor: teal
    type: card
    description: "관심 있어 찾아보고 새로 알게 된 내용을 정리합니다."
    header: 
      title: Interests 😚
      hlcolor: "#8bc34a"
      color: '#fff'
      fontSize: 32
      width: 210 
    cards:
      - subtitle: Linux kernel
        subtitlePosition: center
        description: "시스템 성능 튜닝 아이디어를 얻기 위한 리눅스 커널 코드 분석 내용을 정리하는 스터디 노트입니다."
        image: images/section/100kHz.svg
        color: white
        button: 
          name: Linux kernel
          link: https://paranlee.github.io/linux-kernel/
          size: large
          target: _blank
          color: 'white'
          bgcolor: '#283593'
      - subtitle: Data pipeline
        subtitlePosition: center
        description: "분산 컴퓨팅 아키텍쳐에서 데이터 수집, 적재, 처리, 분석 파이프라인 관련 연구 노트입니다. \n이파란 커리어의 메인 도메인입니다."
        image: images/section/distributed-computing.png
        color: white
        button: 
          name: Data pipeline
          link: https://paranlee.github.io/data-pipeline/
          size: large
          target: _blank
          color: 'white'
          bgcolor: '#283593'
      - subtitle: Softcore
        subtitlePosition: center
        description: "하드웨어 가속화 범용을 위해 마이크로 아키텍쳐를 소프트웨어적으로 다루는 연구 노트입니다."
        image: images/section/softcore.png
        color: white
        button: 
          name: Softcore
          link: https://paranlee.github.io/softcore
          size: large
          target: _blank
          color: 'white'
          bgcolor: '#283593'
  - bgcolor: DarkSlateBlue
    type: normal
    description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce id eleifend erat. Integer eget mattis augue. Suspendisse semper laoreet tortor sed convallis. Nulla ac euismod lorem"
    header:
      title: I love opensource! 😘
      hlcolor: DarkKhaki
      color: "#fff"
      fontSize: 32
      width: 370
    body:
      subtitle: 지식 공유는 우리 모두의 힘이 됩니다.
      subtitlePosition: left
      description: " 같이 해요. \n commit, push, pull request!"
      color: white
      image: images/section/root-server.png
      imagePosition: left

footer:
  sections:
    - title: Paran Lee's Github
      links:
        - title: Github
          link: https://github.com/paranlee
    - title: IAMROOT.ORG
      links:
        - title: IAMROOT.ORG
          link: http://www.iamroot.org/xe/
#    - title: Features
#      links:
#        - title: GitHub
#          link: https://gohugo.io/
  contents: 
    align: left
    applySinglePageCss: false
    markdown:
      |
      ## Paran Lee's document blog
      Copyright © 2021. All rights reserved.
---
