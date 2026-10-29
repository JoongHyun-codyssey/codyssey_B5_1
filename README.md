# 정보를 엄청 빠르게 찾아주는 작은 저장소 만들기

Python으로 해시맵, 이중 연결 리스트, 최소 힙을 직접 구현하고, 이를 이용해 CLI 기반 Key-Value 저장소를 만드는 Codyssey 프로젝트다.

키는 물건을 찾기 위한 이름표, 값은 그 이름표에 연결된 내용이라고 생각하면 된다. 예를 들어 `user:1`이라는 키에 `Alice`라는 값을 저장한다.

## 현재 상태

- 전체 기능 구현 진행률: **5%**
- 완료: 노드 구조, 빈 이중 연결 리스트 초기화, `insert_front`
- 준비 완료: README와 역할별 Python 파일
- 나머지 파일은 역할을 설명하는 docstring만 있는 준비 파일이다.
- CLI와 나머지 명령어는 아직 구현하지 않았다.

진행률은 아래의 작업 비중에 따른 구현·동작 확인 기준이며, 공식 평가 점수가 아니다. 문서와 파일 준비만으로 기능 진행률을 올리지 않는다.

## 프로젝트 구조

프로젝트 폴더 이름은 `mini_redis`다. 모듈은 관련 코드를 모아 둔 Python 파일을 뜻한다.

| 파일 | 역할 |
| --- | --- |
| [README.md](README.md) | 프로젝트 요구사항, 구조, 실행 방법, 진행 상황 |
| [doubly_linked_list.py](doubly_linked_list.py) | 노드와 이중 연결 리스트 구현 |
| [hash_map.py](hash_map.py) | 직접 만든 해시 함수와 체이닝 방식의 해시맵 구현 |
| [min_heap.py](min_heap.py) | 만료 시각이 가장 이른 항목을 찾는 최소 힙 구현 |
| [mini_redis.py](mini_redis.py) | 자료구조를 조합한 데이터 저장, 명령어 처리, LRU, TTL, 메모리 관리 |
| [main.py](main.py) | 사용자 입력, 명령어 파싱, 실행 요청, 결과 출력, 종료 처리 |

완성된 프로그램에서는 `main.py`가 입력을 받고 `mini_redis.py`에 실행을 요청한다. `mini_redis.py`는 직접 만든 자료구조를 사용해 요청을 처리한다.

## 제약사항

- `dict`, `set`, `collections`를 사용하지 않는다.
- `list`는 필요한 배열 저장소로만 제한적으로 사용한다. 배열 생성과 인덱스 접근을 바탕으로 해시맵과 힙의 동작을 직접 구현한다.
- 해시 함수, 충돌 처리, 버킷 확장, 노드 연결, 힙 정렬 과정을 직접 구현한다. `heapq`로 최소 힙을 대신하지 않는다.
- 각 자료구조는 독립된 모듈에 둔다.
- 핵심 클래스와 함수에는 주석 또는 docstring을 작성한다.
- 네트워크 통신, 데이터 영속성, Redis 복잡 자료형(List/Set/Sorted Set), 멀티스레딩과 락을 구현하지 않는다.
- 기능은 제공된 과제 요구사항으로 한정한다.

## 직접 구현할 자료구조

| 자료구조 | 필수 메서드와 필드 | 구현 조건 |
| --- | --- | --- |
| 이중 연결 리스트 | 노드의 `prev`, `next`, `data`; `insert_front`, `insert_back`, `remove_front`, `remove_back`, `remove_node`, `move_to_front` | 모든 삽입·삭제·이동 연산 O(1) |
| 체이닝 해시맵 | `put`, `get`, `remove`, `contains`, `keys`, `size` | 직접 만든 해시 함수, 체이닝으로 충돌 처리, 로드 팩터가 0.75를 초과하면 버킷 수를 2배로 확장 |
| 최소 힙 | `push`, `pop`, `peek`, `size`, `_heapify_up`, `_heapify_down` | `(expire_at, key)` 형태의 항목을 다루며 가장 이른 만료 시각을 빠르게 확인 |

## 구현할 명령어

| 명령어 | 동작과 출력 |
| --- | --- |
| `SET key value` | 값을 저장하고 성공 시 `OK`. 성공하면 LRU를 갱신한다. 기존 키를 덮어쓰면 TTL을 초기화한다. |
| `GET key` | 값이 있으면 `"value"`, 없거나 만료됐으면 `(nil)`. 조회에 성공한 경우에만 LRU를 갱신한다. |
| `DEL key` | 삭제하면 `(integer) 1`, 없으면 `(integer) 0`. 데이터·TTL·LRU를 함께 정리한다. |
| `EXISTS key` | 존재하면 `(integer) 1`, 없으면 `(integer) 0`. |
| `DBSIZE` | 현재 키 개수를 `(integer) N`으로 반환한다. |
| `KEYS` | 전체 키를 번호가 있는 배열 형태로 출력한다. 순서와 정렬은 요구하지 않으며 패턴 매칭은 구현하지 않는다. |
| `CONFIG SET maxmemory bytes` | 0 이상의 정수로 한도를 설정하고 `OK`를 반환한다. 0은 무제한이다. |
| `INFO memory` | `used_memory`, `maxmemory`, `evicted_keys`를 출력한다. |
| `EXPIRE key seconds` | 존재하면 만료 시간을 설정하고 `(integer) 1`, 없으면 `(integer) 0`. 0초 이하는 즉시 삭제한다. |
| `TTL key` | 키가 없으면 `(integer) -2`, 만료 시간이 없으면 `(integer) -1`, 있으면 남은 초를 반환한다. |

`KEYS`의 결과가 비어 있으면 `(empty array)`를 출력한다. 값 입력은 큰따옴표로 감싼 형태를 지원하도록 구현한다.

## 메모리와 LRU 규칙

메모리 사용량은 모든 키와 값을 UTF-8 바이트로 바꿨을 때의 길이를 합한 값이다.

`used_memory = Σ(len(key.encode("utf-8")) + len(value.encode("utf-8")))`

노드, 참조, 버킷 등 자료구조 자체의 메모리는 계산하지 않는다.

- `maxmemory > 0`이고 SET 이후 사용량이 한도를 넘으면, 가장 오래 사용하지 않은 키부터 제거한다.
- 사용량이 한도 이하가 될 때까지 제거하고 매번 `used_memory`를 갱신한다.
- LRU로 제거한 키 개수는 `evicted_keys`에 누적한다.
- 키 하나와 값 하나의 바이트 합만으로 한도를 넘으면 저장하지 않고 OOM 에러를 반환한다.

## TTL 규칙

- 키를 사용하는 명령어는 만료 여부를 먼저 확인한다. 만료된 키는 삭제하고 없는 키처럼 처리한다.
- 만료된 키를 GET하면 삭제 후 `(nil)`을 반환하며 LRU를 갱신하지 않는다.
- SET으로 기존 값을 덮어쓰면 기존 TTL을 초기화한다.
- 없는 키에 EXPIRE를 실행하면 `(integer) 0`을 반환한다.
- DEL은 데이터·TTL·LRU에서 해당 키를 함께 정리한다.
- 최소 힙을 사용해 가장 이른 만료 시각을 빠르게 찾는다.

## CLI와 에러 출력

프롬프트는 `mini-redis>`다. 입력, 파싱, 실행, 결과 출력을 반복하고 `exit` 또는 `quit`으로 종료한다.

| 상황 | 출력 |
| --- | --- |
| 모르는 명령어 | `(error) ERR unknown command '<cmd>'` |
| 인자 개수 오류 | `(error) ERR wrong number of arguments for '<cmd>' command` |
| 정수 파싱 또는 범위 오류 | `(error) ERR value is not an integer or out of range` |
| 단일 항목이 메모리 한도를 초과함 | `(error) OOM command not allowed when used_memory > 'maxmemory'` |

## 실행 방법

Python 3을 사용한다. **아래 명령은 CLI 구현을 완료한 뒤 사용하는 실행 명령이다.**

프로젝트 폴더에서 실행한다.

```bash
python3 main.py
```

현재 `main.py`는 준비 파일이므로 실행해도 CLI 프롬프트가 나오지 않는다.

## 구현 순서와 진행률

| 순서 | 단계 | 전체 비중 | 현재 상태 |
| --- | --- | --- | --- |
| 1 | 이중 연결 리스트 | 20% | 노드와 insert_front 완료: 전체 중 5% |
| 2 | 체이닝 해시맵과 버킷 확장 | 20% | 미구현 |
| 3 | 최소 힙 | 10% | 미구현 |
| 4 | String 기본 명령어 6개 | 15% | 미구현 |
| 5 | 메모리 계산, LRU, 메모리 명령어 | 15% | 미구현 |
| 6 | TTL과 만료 처리 | 10% | 미구현 |
| 7 | CLI, 에러 처리, 전체 요구사항 검증 | 10% | 미구현 |

설명과 구현은 노드 구조 → insert_front → insert_back → 나머지 연결 리스트 연산 순서로 진행한다. 각 부분은 쉬운 비유, 코드 설명, 동작 확인, 동료에게 설명할 핵심 순서로 학습한다.

## 설명할 수 있어야 하는 내용

- 해시 함수가 버킷 위치를 정하는 방법과, 충돌을 체이닝으로 처리하는 방법
- 해시맵으로 노드를 찾고 이중 연결 리스트에서 이동시켜 O(1) LRU 추적을 하는 이유
- 최소 힙이 만료 시간이 가장 빠른 키를 찾는 데 적합한 이유
- 메모리 한도를 넘었을 때 LRU로 키를 제거하고 used_memory를 갱신하는 흐름

