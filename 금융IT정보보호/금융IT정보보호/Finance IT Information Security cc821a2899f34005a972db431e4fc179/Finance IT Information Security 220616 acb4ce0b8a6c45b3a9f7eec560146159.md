# Finance IT Information Security 220616

주 내용 - 네트워크 보안 기술. (여기서 시험 거의 다 나올것임.)

## p59. TCP/IP 프로토콜의 이해

ARPA(미 국방과학연구소 산하 국방과학연구소)넷.의 핵심은 Socket을 제공해서 이기종 네트워크 간 호환성 있는 연결을 하는 것. 이 ARPAnet은 TCP/IP와 Milnet으로 분리됨.

Socket은 TCP와 IP로 구분되고, UDP가 추가됨. TCP/IP는 발전해서 ‘80후반 OSI 모델로 정리됨.

초기엔 프로토콜 필요없었음. → 모두가 유닉스를 쓰니까. unix unit copy (uu cp)

but, 다른 기종 생기면서 프로토콜이 필요해짐. (연결을 위한 상호 규약)

초기 프로토콜 우후 죽순 발생- 보안문제 발생

1. 파일전송 프로토콜: FTP(File Transfer Protocol)
2. 메세지전송 프로토콜: SMTP
3. TELNET

프로토콜의 표준을 제정. OSI 7 Layer.

인터넷 모델

- TCP/IP: 무료 ⇒ De Facto 드팩토.(사실상 표준)

TCP/Ip 4 스택

Ethernet 

IP - ip address와 라우팅, ICMP - Internet Control Message Protocol(***), ARP Address Resolution Protocol - ip address를 mac address로변환

TCP - 연결지향. 전송을 컨트롤. Connection Oriented. 대부분 TCP. 간혹가다 UDP 사용

FTP, Telnet(원격 시스템에 연결해서 시스템 사용할 수 있게함.), 

L1 Physical-비트.(전기가 흐르면 1, 아니면 0) 더미허브,리피터 - 2000년대 생산중단됨. 요새 집에는 다 스위치, L2(***) switch 실제 물리적 연결주소(Mac Media access control address) - 계층 단위 Frame, L3 router(TTL*값에 따라 패킷을 죽이고, 소스IP에 알리는 역할도 진행.) 논리적 연결.IP - 계층단위 Packet, L4 switch(포트적용) - Segment

*TTL - TimetoLive. 패킷이 Destination에 못가고 계쏙 라우터를 돌면 안되므로, 라우터를 돌 최대 수를 지정해주는 것. 최대치에 도달하면 해당 라우터는 패킷을 죽이고, 소스IP에 본인 IP와 죽였다는 정보를 보냄.

Telnet - TCP포트 23번. 금지

P.T(Plain Text) - 평문 → 스니핑 용이

⇒ 암호화 전송 SSH (Secure SHell)

FTP ⇒ SFTP(Secure FTP) 22/TCP Port    는 SSH에 포함되어있음.

FTP - TCP포트 20번, 21번

SMTP - TCP포트 25번.

포트는 프로세스(프로그램) 간의 연결. IP는 호스트 간의 연결!!!!!!!!!!!

사용자가 웹브라우저를 활용해 서버에 접속하는 프로세스

7층 → 1층 ⇒ 1층 → 7층

ip로 들어가서 80번 웹서버 포트로 들어감.

session이란 소스(Client)의 IP와 소스의 Port(웹브라우저 사용시 포트를 하나 할당받음)가

destination(Server)의 ip와 port에 연결이 됐을때. 이를 세션이라고 함.

**Spoofing(둔갑)**을 하는 목적: **Sniffing(패킷 교환을 엿듣는 것)**을 하려고.

스위치는 스니핑이 어려움. 더미허브(길1개)와는 다르게 루트가 많음.

패킷 - 6개의 상태플러그

네트웍 설정 (Host Configuration)

1. 수동.  - 명령어 ipconfig - /displaydns flushdns, ping - 인트라넷에서 사용불가, tracert, nslookup, arp - -a 캐싱된 내용 다 보여줘.

1) 유일한 IP 어드레스 할당 

2) 넷마스크값 ⇒ LAN

3) GateWay(L7) Address (라우터(L3) IP) 

4) DNS 서버(도메인이름 → IP 어드레스 변환 서비스를 지원)  - 공유기

1. 자동 ⇒ DHCP (Dynamic Host Configuration Protocol) - IP공유기, AP

**사설(내부) IP**  

IP**v4 (version4) ⇒ 32bit - 2의 32승 43억개.** 

43억개론 관리가 힘들어 클래스를 나눔.

A class 10.H.H.H (H -host부분은 내가 지정 가능.) 2의 24승개. 16백만대. 우리나라에 없음.

B Class 172.16 ~172.31 N.N.H.H → 2의 16승. 6만5천. 국공립대 같은곳에 간혹 있음.

C class 192.168.0 ~ 192.168.25 N.N.N.H → 2의 5승. 250개. 대부분 C클래스.

서브넷마스크 - 네트웍의 경계

**ARP 스푸핑, MAC 스푸핑 나올수도 있음**

Lan에서는 ip가 아닌 물리적주소인 mac주소로 연결.  miTm man in the middle. for snipping

암호화

- 서비스

SSL(프로토콜에 S가붙으면 이거.)/TLS, 켈베로스

- 연결

SSH,VPN

## p71. UDP Flooding, 서비스 거부 공격 TCP SYN flooding

3handshake.

3세대 Firewall

리눅스의 IPtable