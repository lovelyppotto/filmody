# filmody

film + melody

<hr />

# 1. 프로젝트 소개

### 1) 개발 기간

   : 2024. 11. 15 ~ 2024 . 11. 26 (12일)

### 2) 개발 인원
  - 정주은
  - 윤지원

### 3) 프로젝트 내용

  - 영화 추천 및 관련 플레이리스트 생성 & 공유 웹 사이트

### 4) 기술 스택

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=Django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=SQLite&logoColor=white)
![Vue.js](https://img.shields.io/badge/Vue.js-4FC08D?style=for-the-badge&logo=Vue.js&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=Bootstrap&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=HTML5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=CSS3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=JavaScript&logoColor=black)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white)


# 2. 주요 기능
### 1. 유저 관리
1.1 회원가입

필수 입력 정보
- 아이디
- 비밀번호
- 비밀번호 확인
- 닉네임
- 이메일


회원가입 시 기본 프로필 이미지 자동 설정
모든 입력값에 대한 유효성 검사 진행
가입 완료 시 자동 로그인 및 홈 화면 리다이렉트

1.2 회원 탈퇴
보안을 위한 비밀번호 재확인 절차

1.3 회원 정보 수정
프로필 페이지에서 수정 페이지로 이동
수정 가능 항목
- 비밀번호
- 이메일
- 닉네임
- 프로필 사진 (추가/수정/삭제)
- 리뷰 표시 설정

### 2. 인증

로그인/로그아웃 기능
로그아웃 시 홈 화면으로 자동 리다이렉트

### 3. 프로필

사용자 제작 플레이리스트 목록 표시
팔로우 기능

팔로워/팔로잉 수 표시
팔로우 상태에 따른 버튼 UI 변경


좋아요한 콘텐츠 목록

플레이리스트
영화



### 4. 홈 화면


4.2 네비게이션 바
비로그인 시: 회원가입, 로그인
로그인 시: 프로필, 로그아웃

공통 메뉴
홈
라이브러리
플레이리스트
추천 영화
프로필



### 5. 검색 기능

영화 검색 지원 (제목, 검색명)
검색 결과 클릭 시 영화 상세 페이지로 이동

### 6. 영화 추천

KOBIS API(주간 박스오피스), KMDB API(영화 상세 정보) 사용
영화 상세페이지에서 좋아요 기능

### 7. 라이브러리
로그인 사용자 전용
YouTube API 연동

주요 섹션
- 내 플레이리스트
- 좋아요한 플레이리스트
- 좋아요한 영화 목록

### 8. 플레이리스트 (커뮤니티)
8.1 플레이리스트 목록

최신순 정렬 제공

8.2 플레이리스트 관리

새 플레이리스트 생성
YouTube 검색 통한 컨텐츠 추가
본인 생성 플레이리스트 삭제 권한

8.3 리뷰 시스템

플레이리스트 리뷰 작성
리뷰 좋아요 기능 (자신의 리뷰 제외)
스포일러 방지를 위한 리뷰 가리기 옵션

### 9. 챗봇

영화 추천 AI 챗봇
사용자 검색어 기반 영화 추천
OPENAI API 사용


📝 API 연동
KOBIS API: 박스오피스 정보 제공
KMDB API : 영화 상세 정보 제공
YouTube API: 플레이리스트 관련 기능
OPENAI API : 챗봇 관련 기능 제공



# 11/19

- fixtures 데이터 만드는 데에 있어서 자꾸 environ 이 설치되어 있지 않다는 문구가 떴었습니다.
  환경 설정 문제로 같은 문제가 발생하면 환경변수 및 전역 설치 여부 등을 확인해야 한다는 것을 알았습니다.
- git push 전 제대로 동작하는 것 확인하고 올리기...!(중요)

- 플레이리스트 리뷰 모델
 class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'playlist']
        -> 이런식으로 하면 중복작성 불가능하게 제한 가능함..!

# 11/20
- fixtures 데이터 만들 때 만약 한 필드 내에 여러 요소가 있을 경우...
  해당 필드가 타 데이터의 외래키로 쓰일 때 오류난다
  외래키 -> many to many 필드로 전환하면 쉽게 해결 가능!
  대신 fixtures 해당 데이터를 배열 형태로 전환해줘야 한다
- 백엔드 구현에 문제가 없을 때 vue console에 html 내역이 넘어오는 경우...
  해당 데이터 받아오는 url에 문제 있을 가능성이 높음
- 로그인 새로고침 시 유지가 안될 때
  npm install vuex-persistedstate를 설치해주어야 한다.


# 팀원 정보 및 업무 분담 내역
 정주은
 1. 로그인, 로그아웃 기능
 2. 회원가입 기능	정주은
 3. 영화 상세 목록 조회
 4. 영화 목록 조회
 5. 좋아요 기능
 6. 팔로우 기능
 7. 프로필 조회 기능
       
 윤지원
 1. 영화 데이터 (최소 50개 이상)	윤지원
 2. 영화 목록 조회
 3. 커뮤니티 게시글 기능
 4. 커뮤니티 댓글 기능
 5. 좋아요 기능	
 6. 영화 추천 알고리즘	윤지원
 7. AI (챗봇) 기능	윤지원
