+++
author = "Paran Lee"
title = "overview"
date = "2021-03-01"
description = "hash 기반 Join 을 위해 빠르게 동작하는 확률적 자료구조"
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
series = ["Data pipeline"]
+++

## why?

왜 Join 에서 nested loop (반복문 중첩) 대신 사용할까?

<!--more-->

## Bloom filter

확률적 자료구조?

#### Bloom filter Code block
{{< highlight c >}}
/** ***************************************************************************
 * Structure to keep track of one bloom filter.  Caller needs to
 * allocate this and pass it to the functions below. First call for
 * every struct must be to bloom_init().
 *
 */
struct bloom
{
  // These fields are part of the public interface of this structure.
  // Client code may read these values if desired. Client code MUST NOT
  // modify any of these.
  int entries;
  double error;
  int bits;
  int bytes;
  int hashes;

  // Fields below are private to the implementation. These may go away or
  // change incompatibly at any moment. Client code MUST NOT access or rely
  // on these.
  double bpe;
  unsigned char * bf;
  int ready;
};
{{< /highlight >}}
