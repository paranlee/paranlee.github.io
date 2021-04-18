Linux 커널에서 페이지 교체를 다음 두 가지 방법 중 하나로 처리합니다.

1) kswapd 를 통한 Asynchronously,
2) direct reclaim 를 통한 Synchronously

페이지 할당 시간에 할당 작업은 zone 구조체 인스턴스의 freelist 멤버에 등록했던 페이지를 즉시 받게되므로 수행 중이던 작업을 바로 다시 작업 할 수 있습니다. 직간접적으로 비즈니스 로직(메모리 할당한 프로그램)을 실행한다고 봅니다. (메모리 할당 오버헤드가 거의 없음)

1) kswapd 를 통한 Asynchronously

페이지 할당을 작업을 확실히 끝 마치기 직전에, 사용 가능한 페이지가 zone low watermark 에 도달한지 확인하고 만약 그렇다면 kswapd 가 깨어납니다. Kswapd (Kswapd wake up API 내부에 kcompactd 를 깨우는 루틴이 있음)는 새 페이지 할당을 위한 공간을 만들기 위해 제거 할 비활성 페이지를 찾는 작업인 페이지 스캔을 시작합니다. kswapd 작업을 통해 기존 작업은 지연 시간이 없이 각자의 zone 의 멤버인 freelist 목록에서 메모리를 계속 할당 할 수 있습니다.

2) direct reclaim 를 통한 Synchronously

사용 가능한 페이지에 대한 수요가 kswapd 작업이 공급 할 수 있는 수준을 초과하면 페이지 할당이 다르게 작동합니다. 할당 작업에서 사용 가능한 페이지 수가 해당 zone 의 min watermark 이하인 것을 확인하면 작업은 더 이상 zone 의 freelist 멤버 목록에서 페이지를 가져 오지 않습니다. 그 대신에, 작업은 kswapd 와 동일한 CPU-bound 루틴(각 CPU 와 해당하는 zone 에 한정적인 루틴들)을 실행하여 페이지를 스캔하고 제거하여 자체 할당을 충족합니다. 이것을 direct reclaim (직접 회수)라고 합니다.

직접 회수를 수행하는 데 소요되는 시간은 상당 할 수 있으며, 종종 작은 order0 할당의 경우 수십 ~ 수백 밀리 초가 걸리고 order9 거대한 페이지 할당의 경우 0.5 초 이상이 걸립니다.

사실, 리눅스 시스템에서는 kswapd 가 실제로 필요하지 않습니다.

직접 회수를 방지하여 성능을 최적화하기 위한 목적으로만 존재합니다.

메모리 부족 현상이 직접 회수를 트리거하기에 충분하면 시스템에서 실행 중인 모든 작업에서 발생할 수 있습니다. 하나의 공격적인 메모리 할당 작업은 추가 메모리를 거의 할당하지 않는 소규모 작업에 이차적인 데미지를 줄 수 있습니다. nscd(name service cache daemon, DNS name 검색 시에 캐시 역할을 함. DNS 를 지속적으로 사용한다면 사용하지 않을 때, 체감 상으로도 굉장한 속도 차이를 느낄 수 있음) DNS Qeury 를 캐싱하기 위해 메모리를 할당할 때  추가 지연 시간을 100ms나 주입하는 상황을 고려해보면 어떨까요.

재시도 폭풍(retry storms) -> 과도응답(overshoot)


mm: Support multiple kswapd threads per node - Buddy Lumpkin 에서 발췌함
@ 2018-04-02  9:24

- https://lore.kernel.org/lkml/A1EF8129-7F59-49CB-BEEC-E615FB878CE2@oracle.com/T/