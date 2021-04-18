2.1 A Taxonomy of Parallel Computing

병렬 컴퓨팅의 분류

Beowulf-class systems — ensembles of PCs (e.g., Intel Pentium 4) integrated with commercial COTS local area networks (e.g., Fast Ethernet) or system area networks (e.g., Myrinet) and run widely available low-cost or no-cost software for managing system resources and coordinating parallel execution. Such systems exhibit exceptional price/performance for many applications.

상용 COTS(기성) LAN (예 : 고속 이더넷) 또는 시스템 영역 네트워크 (예 : Myrinet)와 통합 된 PC 앙상블 (예 : Intel Pentium 4) 및 시스템 리소스 관리 및 조정을 위해 널리 사용되는 저비용 또는 무료 소프트웨어 실행 병렬 실행. 이러한 시스템은 많은 애플리케이션에서 탁월한 가성비를 보여줍니다.

Superclusters — clusters of clusters, still within a local area such as a shared machine room or in separate buildings on the same industrial or academic campus, usually integrated by the institution’s infrastructure backbone wide area netork. Although usually within the same internet domain, the clusters may be under separate ownership and administrative responsibilities. Nonetheless, organizations are striving to determine ways to enjoy the potential opportunities of partnering multiple local clusters to realize very large scale computing at least part of the time.

일반적으로 기관의 인프라 백본 광역 네트워크로 통합되는 동일한 산업 또는 학술 캠퍼스의 별도 건물 또는 공유 머신룸과 같은 로컬 영역 내에 있는 클러스터 집단의 클러스터 집단입니다. 일반적으로 동일한 인터넷 도메인 내에 있지만 각 클러스터들은 별도의 소유권 및 관리 책임을 가질 수 있습니다. 그럼에도 불구하고, 조직은 적어도 일부 시간 동안 대규모 컴퓨팅을 실현하기 위해 여러 로컬 클러스터와 파트너 관계를 맺을 수있는 잠재적 기회를 누릴 수있는 방법을 결정하기 위해 노력하고 있습니다.


3.3.2.6 Distribute Jobs Tasks Across Allocated Resources

With the resources selected, Maui then maps job tasks to the actual resources.
This distribution of tasks is typically based on simple task distribution algorithms such as round-robin or max blocking, but can also incorporate parallel language library (i.e., MPI, PVM, etc) specific patterns used to minimize interprocesses communication overhead.

3.3.2.6 할당 된 리소스에 작업 작업 배포

선택한 리소스로 Maui는 작업 태스크를 실제 리소스에 매핑합니다.
이러한 작업 배포는 일반적으로 라운드 로빈 또는 최대 차단과 같은 간단한 작업 배포 알고리즘을 기반으로하지만 프로세스 간 통신 오버 헤드를 최소화하는 데 사용되는 병렬 언어 라이브러리 (예 : MPI, PVM 등) 특정 패턴을 통합 할 수도 있습니다.

8.3 Node Set Overview

While backfill improves the scheduler's performance, this is only half the battle.
The efficiency of a cluster, in terms of actual work accomplished, is a function of both scheduling performance and individual job efficiency.
In many clusters, job efficiency can vary from node to node as well as with the node mix allocated.
Most parallel jobs written in popular languages such as MPI or PVM do not internally load balance their workload and thus run only as fast as the slowest node allocated.
Consequently, these jobs run most effectively on homogeneous sets of nodes. However, while many clusters start out as homogeneous, they quickly evolve as new generations of compute nodes are integrated into the system.
Research has shown that this integration, while improving scheduling performance due to increased scheduler selection, can actually decrease average job efficiency.

8.3 노드 세트 개요

backfill 은 스케줄러의 성능을 향상 시키지만 이것은 절반에 불과합니다.
실제 수행 한 작업 측면에서 클러스터의 효율성은 일정 성능과 개별 작업 효율성의 함수입니다.
많은 클러스터에서 작업 효율성은 할당 된 노드 조합뿐 아니라 노드마다 다를 수 있습니다.
MPI 또는 PVM과 같이 널리 사용되는 언어로 작성된 대부분의 병렬 작업은 내부적으로 작업 부하를 분산하지 않으므로 할당 된 가장 느린 노드만큼 빠르게 실행됩니다.
결과적으로 이러한 작업은 동종 노드 집합에서 가장 효과적으로 실행됩니다. 그러나 많은 클러스터가 동종으로 시작하지만 새로운 세대의 컴퓨팅 노드가 시스템에 통합됨에 따라 빠르게 발전합니다.
연구에 따르면 이러한 통합은 스케줄러 선택 증가로 인해 스케줄링 성능을 향상시키면서 실제로 평균 작업 효율성을 감소시킬 수 있습니다.





The Maui Scheduler can be thought of as a policy engine which allows sites control over when, where, and how resources such as processors, memory, and disk are allocated to jobs.
In addition to this control, it also provides mechanisms which help to intelligently optimize the use of these resources, monitor system performance, help diagnose problems, and generally manage the system.


Maui Scheduler는 프로세서, 메모리 및 디스크와 같은 리소스가 작업에 할당되는시기, 위치 및 방법을 사이트에서 제어 할 수있는 정책 엔진으로 생각할 수 있습니다.
이 제어 외에도 이러한 리소스의 사용을 지능적으로 최적화하고, 시스템 성능을 모니터링하고, 문제를 진단하고, 일반적으로 시스템을 관리하는 데 도움이되는 메커니즘을 제공합니다.

Running multi-site MPI jobs with Maui and MPICH Two things need to happen in order to run multi-site MPI jobs:

Nodes must be reserved and jobs must be run in a coordinated manner.
Jobs must be started such that they are set to communicate with with each other using MPI calls.
The meta scheduling interface to the Maui Scheduler can be used to reserve nodes and start jobs across distributed sites.
MPICH can be used to enable separate jobs to communicate with each other using MPI.

Flow:

A job is submitted to the meta scheduler.
The meta scheduler communicates with separate Maui schedulers to determine node availability.
The meta scheduler starts an individual job at each site. Each job consists solely of an MPICH ch_p4 server process running on each of the job's nodes.
The meta scheduler creates an MPICH proc group file, with hostname and executable information for each site. An MPICH job is started using the proc group file.
One MPICH process runs on the submitting host. 
This process communicates through ch_p4 servers to start MPICH processes on all nodes specified.

Maui 및 MPICH로 다중 사이트 MPI 작업 실행 다중 사이트 MPI 작업을 실행하려면 다음 두 가지가 수행되어야합니다.

노드는 예약되어야하며 작업은 조정 된 방식으로 실행되어야합니다.
작업은 MPI 호출을 사용하여 서로 통신하도록 설정되도록 시작되어야합니다.
Maui Scheduler에 대한 메타 스케줄링 인터페이스는 분산 된 사이트에서 노드를 예약하고 작업을 시작하는 데 사용할 수 있습니다.
MPICH를 사용하면 별도의 작업이 MPI를 사용하여 서로 통신 할 수 있습니다.

흐름:

작업이 메타 스케줄러에 제출됩니다.
메타 스케줄러는 별도의 Maui 스케줄러와 통신하여 노드 가용성을 결정합니다.
메타 스케줄러는 각 사이트에서 개별 작업을 시작합니다. 각 작업은 각 작업의 노드에서 실행되는 MPICH ch_p4 서버 프로세스로만 구성됩니다.
메타 스케줄러는 각 사이트에 대한 호스트 이름 및 실행 가능 정보와 함께 MPICH proc 그룹 파일을 생성합니다. MPICH 작업은 proc 그룹 파일을 사용하여 시작됩니다. 하나의 MPICH 프로세스가 제출 호스트에서 실행됩니다. 이 프로세스는 ch_p4 서버를 통해 통신하여 지정된 모든 노드에서 MPICH 프로세스를 시작합니다.

Setup:

A user account must be created at each site. The job executable and data must be created at each site.
MPICH must be installed at each site, and on the submitting host.
It should be configured to use the ch_p4 device. The executable path must be added to the ~/.server_apps file for the user at each site.
The submitting host and user must be added to the .rhosts file for each site.
A meta job specification, detailing username and executable name for each site should be created.


설정:

각 사이트에서 사용자 계정을 만들어야합니다. 작업 실행 파일과 데이터는 각 사이트에서 생성되어야합니다.
MPICH는 각 사이트와 제출 호스트에 설치해야합니다.
ch_p4 장치를 사용하도록 구성해야합니다. 실행 경로는 각 사이트에서 사용자의 ~ / .server_apps 파일에 추가되어야합니다.
제출 호스트 및 사용자는 각 사이트의 .rhosts 파일에 추가되어야합니다.
각 사이트의 사용자 이름과 실행 파일 이름을 자세히 설명하는 메타 작업 사양을 만들어야합니다.


# TORQUE for job submission

# Maui for job scheduling

1	Overview
    1.1	Queue Structure
    1.2	Node-Queue Matrix
    2	Job Submission
    2.1	Example Interactive Job
    2.2	Example Script
3	Job Control
4	Examples
    4.1	Serpent2
    4.2	Nuclear data
    4.3	MCNPX
    4.4	MCNP5
    4.4.1	MPI Only
    4.4.2	OpenMP Only
    4.4.3	MPI and OpenMP
    4.5	MCNP6.1
    4.6	MCNP6.2
    4.7	MCNP: Delete unneeded runtapes
    4.8	Scale
    4.9	Advantg
5	FAQ
    5.1	How can I setup unique temporary directory for my job?
    5.2	I'm not getting error/output files!
    5.3	How can I request different CPU counts on different nodes/How can I use multiple queues?
    5.4	How can I submit a job to a specific node?
    5.5	How can I ensure that I have enough *local* disk space (in /tmp)?
    5.6	I messed up my node allocation request! How do I fix it?
    5.7	Where are my jobs?
    5.8	Admin stuff