# filmody

film + melody

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
