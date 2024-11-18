import json
import requests
from datetime import datetime, timedelta
import time
from django.conf import settings

class MovieFixturesCreator:
    def __init__(self):
        self.kobis_key = settings.KOBIS_API_KEY
        self.kmdb_key = settings.KMDB_API_KEY
    
    def get_movie_details_from_kobis(self, movie_cd):
        """영화진흥위원회 API에서 영화 상세정보 조회"""
        kobis_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json"
        params = {
            'key': self.kobis_key,
            'movieCd': movie_cd
        }
        
        response = requests.get(kobis_url, params=params)
        movie_data = response.json()
        return movie_data.get('movieInfoResult', {}).get('movieInfo', {})

    def get_movie_details_from_kmdb(self, movie_title, directors=None, opendt=None):
        """KMDB API에서 영화 상세정보 조회 - 여러 조건으로 검색"""
        kmdb_url = "http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp"
        
        # 기본 검색 파라미터
        params = {
            'ServiceKey': self.kmdb_key,
            'collection': 'kmdb_new2',
            'title': movie_title,
            'detail': 'Y'
        }
        
        # 개봉일이 있으면 추가
        if opendt:
            params['releaseDts'] = opendt.replace('-', '')
            
        response = requests.get(kmdb_url, params=params)
        results = response.json().get('Data', [{}])[0].get('Result', [])
        
        if not results:
            return {}
            
        # 여러 결과가 있을 경우 가장 적절한 결과 선택
        best_match = None
        highest_match_score = 0
        
        for result in results:
            match_score = 0
            
            # 제목 정확도
            if movie_title == result.get('title'):
                match_score += 3
                
            # 감독 일치 여부
            if directors and result.get('directors'):
                kmdb_directors = [d.get('directorNm') for d in result['directors'].get('director', [])]
                if any(d in kmdb_directors for d in directors):
                    match_score += 2
                    
            # 개봉일 일치 여부
            if opendt and result.get('releaseDts'):
                if opendt.replace('-', '') == result['releaseDts']:
                    match_score += 2
                    
            if match_score > highest_match_score:
                highest_match_score = match_score
                best_match = result
                
        if not best_match:
            best_match = results[0]  # 매칭되는 것이 없으면 첫 번째 결과 사용
            
        return {
            'director': ', '.join(d.get('directorNm', '') for d in best_match.get('directors', {}).get('director', [])),
            'genre': best_match.get('genre', ''),
            'poster_url': best_match.get('posters', '').split('|')[0],
            'plot': best_match.get('plots', {}).get('plot', [{}])[0].get('plotText', ''),
            'actors': ', '.join(a.get('actorNm', '') for a in best_match.get('actors', {}).get('actor', [])[:5]),
            'production_year': best_match.get('prodYear', ''),
            'show_time': best_match.get('runtime', ''),
            'nation': best_match.get('nation', ''),
            'rating': best_match.get('rating', '')
        }

    def create_fixtures(self):
        fixtures_data = []
        boxoffice_list = self.get_weekly_boxoffice()
        
        for index, movie in enumerate(boxoffice_list, start=1):
            print(f"Processing: {movie['movieNm']}")
            time.sleep(0.5)
            
            # 영화진흥위원회 상세정보 조회
            kobis_details = self.get_movie_details_from_kobis(movie['movieCd'])
            
            # 감독 정보 추출
            directors = [director['peopleNm'] for director in kobis_details.get('directors', [])]
            
            # KMDB 정보 조회 - 더 정확한 매칭을 위해 감독명과 개봉일 활용
            movie_details = self.get_movie_details_from_kmdb(
                movie_title=movie['movieNm'],
                directors=directors,
                opendt=kobis_details.get('openDt')
            )
            
            fixture = {
                "model": "movies.movie",
                "pk": index,
                "fields": {
                    "rank": movie['rank'],
                    "title": movie['movieNm'],
                    "audience_acc": int(movie['audiAcc']),
                    "director": movie_details.get('director', ''),
                    "genre": movie_details.get('genre', ''),
                    "poster_url": movie_details.get('poster_url', ''),
                    "plot": movie_details.get('plot', ''),
                    "actors": movie_details.get('actors', ''),
                    "production_year": movie_details.get('production_year', ''),
                    "show_time": movie_details.get('show_time', ''),
                    "nation": movie_details.get('nation', ''),
                    "rating": movie_details.get('rating', ''),
                    "created_at": datetime.now().strftime('%Y-%m-%d')
                }
            }
            
            fixtures_data.append(fixture)
        
        with open('movies/fixtures/initial_data.json', 'w', encoding='utf-8') as f:
            json.dump(fixtures_data, f, ensure_ascii=False, indent=2)
        
        return fixtures_data