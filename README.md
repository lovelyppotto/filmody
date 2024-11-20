# filmody

film + melody

# 11/19

- fixtures 데이터 만드는 데에 있어서 자꾸 environ 이 설치되어 있지 않다는 문구가 떴었습니다.
  환경 설정 문제로 같은 문제가 발생하면 환경변수 및 전역 설치 여부 등을 확인해야 한다는 것을 알았습니다.
- git push 전 제대로 동작하는 것 확인하고 올리기...!(중요)

- # 플레이리스트 리뷰 모델
 class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'playlist']
        -> 이런식으로 하면 중복작성 불가능하게 제한 가능함..!