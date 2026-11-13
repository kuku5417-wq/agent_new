# agent_new — 사내망 개발 동료용 shi 배포

사내망만 쓰는 **개발하는 동료**가 GitHub 없이 shi(공통 에이전트·스킬·가드)를 설치하고 바로 쓰게 하는 묶음이다. shi 자체는 [kuku5417-wq-shi_dev](https://github.com/kuku5417-wq/kuku5417-wq-shi_dev)에서 만들고, 여기서는 **동료용 문서와 배포 zip**만 다룬다.

| 파일 | 누가 | 내용 |
|---|---|---|
| [설치_안내.md](설치_안내.md) | 동료(의 Claude) | zip 풀기 → 준비물 확인 → 설치 → 확인. 사람은 "설치해 줘" 한 마디 |
| [시작_한장.md](시작_한장.md) | 동료 | 지키는 것 다섯 가지, 새 앱 만들기, 돌고 있는 앱 바꾸기 |
| [자주_쓰는_말.md](자주_쓰는_말.md) | 동료 | Claude에게 붙여 넣는 문장 |
| [자주_묻는_것.md](자주_묻는_것.md) | 동료 | 훅 실패, 스킬 이름, 막힘, 0.0.0.0, 업데이트·제거 |
| [배포_절차.md](배포_절차.md) | AX 담당 | 판 고르기 → zip → 시험 설치 → NAS → 안내 페이지 → 알리기 |
| `make_bundle.py` | AX 담당 | shi_dev의 정한 판 + 위 문서 → `dist\shi_사내망_<판>.zip` |

zip 안 구성: 위 동료용 문서 4개 + `사내망_적용.md` + `install_local.py` + `plugins\shi\` + `VERSION`.

## 저장소 지도 (네 저장소가 하는 일)

| 저장소 | 이 PC 폴더 | 하는 일 |
|---|---|---|
| [kuku5417-wq-shi_dev](https://github.com/kuku5417-wq/kuku5417-wq-shi_dev) | `JSH\agent 가이드` | **엔진.** 공통 플러그인 shi(에이전트 8·스킬 10·가드 훅·틀)를 만들고 판(0.4.0 …)을 낸다. 규칙을 바꾸는 곳은 여기 하나 |
| [agent_trans](https://github.com/kuku5417-wq/agent_trans) | `JSH\agent 가이드_trans` | **사외망 → 사내망 넘기기.** 사외망에서 새로 만들거나 이미 만든 앱을 shi 규칙으로 검토·수정해 사내망으로 옮기는 가이드·점검표·사례. 첫 사례 meeting(결정 ①~⑤) |
| [agent_new](https://github.com/kuku5417-wq/agent_new) | `JSH\agent 가이드_new` | **사내망 동료 배포.** GitHub 없는 사내망 개발 동료에게 shi를 zip(NAS·아티팩트)으로 나눠 주는 문서와 `make_bundle.py` |
| [meeting](https://github.com/kuku5417-wq/meeting) | (본인 PC `F:\code\_원본\meeting`) | **원본 보관.** 커미셔닝팀 회의자료 앱(FastAPI) 원본. 고치지 않는다 — 전환 작업은 별도 브랜치·작업본에서 |

흐름: shi_dev가 판을 내면 → agent_trans가 그 판으로 앱을 넘기고, agent_new가 그 판을 동료에게 나눠 준다.
