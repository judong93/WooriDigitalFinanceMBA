# Finance IT Information Security 220617

**침입탐지 시스템이란**

IDS란 컴퓨터 시스템의 비정상적인 사용, 오용, 남용 등을 규정하는 시스템으로 가능한한 실시간(IDS의 한계)으로 침입에 대한 탐지와 처리를 하도록하는 소프트웨어 및 하드웨어를 통칭.

개발배경

- 방화벽만으로 안정성 확보 미흡
- 홈뱅킹, 전자상거래 증가

역할

- 공격 감지
- 위험한 연결 강제종료 (Termination)
- 침입을 보고
- 이벤트 및 연결을 로깅

![Untitled](Finance%20IT%20Information%20Security%20220617%209e813c9f3e064a4ea428adda2bf48bfe/Untitled.png)

![Untitled](Finance%20IT%20Information%20Security%20220617%209e813c9f3e064a4ea428adda2bf48bfe/Untitled%201.png)

## 오용탐지

![Untitled](Finance%20IT%20Information%20Security%20220617%209e813c9f3e064a4ea428adda2bf48bfe/Untitled%202.png)

## 비정상탐지

![Untitled](Finance%20IT%20Information%20Security%20220617%209e813c9f3e064a4ea428adda2bf48bfe/Untitled%203.png)

## IPS

![Untitled](Finance%20IT%20Information%20Security%20220617%209e813c9f3e064a4ea428adda2bf48bfe/Untitled%204.png)

지능형 차단시스템. 

**소셜엔지니어링**

**etc / hosts 파일**

?? 순서.

1.

2.호스트파일에게 물어본다

3.메인서버에게 물어본다

DNS서버 99.9% 는 리눅스.

웹서버

프로덕션(운영)서버 - 실제서비스 제공

샌드박스 서버 - 인터넷망. ⇒ 보안에 있어서 중요함.

스테이징 서버 - 프로덕션 환경과 유사. 실무적 환경과 유사한 곳에서 테스트.(내부망)

테스트 서버 - APP 테스트.

개발용 서버(디벨롭) (대부분 HP UNIX)- APP 개발.

**WAS**

**쿠키**

**세션**

**Web Hacking 이란**

![Untitled](Finance%20IT%20Information%20Security%20220617%209e813c9f3e064a4ea428adda2bf48bfe/Untitled%205.png)

## 대칭키

![Untitled](Finance%20IT%20Information%20Security%20220617%209e813c9f3e064a4ea428adda2bf48bfe/Untitled%206.png)

![Untitled](Finance%20IT%20Information%20Security%20220617%209e813c9f3e064a4ea428adda2bf48bfe/Untitled%207.png)

## 비대칭

![Untitled](Finance%20IT%20Information%20Security%20220617%209e813c9f3e064a4ea428adda2bf48bfe/Untitled%208.png)

디피홀만 ⇒ 비대칭키의 원조. RSA