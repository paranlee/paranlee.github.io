+++
author = "Hugo Authors"
title = "overview"
date = "2021-03-01"
description = "SQL Join 시 빠르게 동작하는 확률적 자료구조"
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

## List Types

#### Ordered List

1. First item
2. Second item
3. Third item

Most <mark>salamanders</mark> are nocturnal, and hunt for insects, worms, and other small creatures.

<!--more-->