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
### 1) 회원가입



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

  -----------------------------------------------------------------------------------------------------
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
