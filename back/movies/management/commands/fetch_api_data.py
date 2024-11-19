from django.core.management.base import BaseCommand
import json
import requests
from datetime import datetime, timedelta
import time
from django.conf import settings
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetch movie data from KOBIS and KMDB APIs and create fixtures'

    def handle(self, *args, **options):
        try:
            creator = MovieFixturesCreator()
            creator.create_fixtures()
            self.stdout.write(self.style.SUCCESS('Successfully created movie fixtures'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to create fixtures: {str(e)}'))

class MovieFixturesCreator:
    def __init__(self):
        self.kobis_key = settings.KOBIS_API_KEY
        self.kmdb_key = settings.KMDB_API_KEY
        self.timeout = 30  # API 요청 타임아웃 설정 증가
        
    def get_weekly_boxoffice(self, max_weeks=10):
        """
        최근 10주간의 박스오피스 데이터와 개봉 1년 이내, 전체관람가 일반 영화를 조합하여 반환
        """
        all_movies = {}

        # 1. 최근 10주간의 박스오피스 데이터 수집
        print("1. Fetching recent boxoffice data...")
        for week in range(max_weeks):
            target_date = (datetime.now() - timedelta(days=7 * (week + 1))).strftime('%Y%m%d')
            try:
                response = requests.get(
                    "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json",
                    params={
                        'key': self.kobis_key,
                        'targetDt': target_date,
                        'weekGb': '0'
                    },
                    timeout=self.timeout
                )
                response.raise_for_status()
                weekly_list = response.json().get('boxOfficeResult', {}).get('weeklyBoxOfficeList', [])
                
                for movie in weekly_list:
                    movie_cd = movie['movieCd']
                    if movie_cd not in all_movies:
                        all_movies[movie_cd] = movie
                
                print(f"Week {week + 1}: Total movies so far: {len(all_movies)}")
                time.sleep(2)
                
            except Exception as e:
                print(f"Error fetching boxoffice for week {week + 1}: {str(e)}")

        # 2. 개봉 1년 이내, 전체관람가 일반 영화 목록 수집
        print("\n2. Fetching general movie list...")
        current_page = 1
        max_pages = 5  # 최대 5페이지까지 시도
        
        while len(all_movies) < 50 and current_page <= max_pages:
            try:
                response = requests.get(
                    "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json",
                    params={
                        'key': self.kobis_key,
                        'itemPerPage': 100,
                        'curPage': current_page,
                        'openStartDt': (datetime.now() - timedelta(days=365)).strftime('%Y%m%d'),
                        'movieTypeCd': '220101',  # 장편영화
                        'watchGradeCd': '210201'  # 전체관람가
                    },
                    timeout=self.timeout
                )
                response.raise_for_status()
                data = response.json()
                movie_list = data.get('movieListResult', {}).get('movieList', [])
                
                added = 0
                for movie in movie_list:
                    if len(all_movies) >= 50:
                        break
                        
                    movie_cd = movie['movieCd']
                    if movie_cd not in all_movies:
                        all_movies[movie_cd] = {
                            'movieCd': movie_cd,
                            'movieNm': movie['movieNm'],
                            'openDt': movie.get('openDt', ''),
                            'audiAcc': '0',
                            'rank': str(len(all_movies) + 1)
                        }
                        added += 1
                
                print(f"Page {current_page}: Added {added} movies. Total: {len(all_movies)}")
                
                if not movie_list:  # 더 이상 결과가 없으면 중단
                    break
                    
                current_page += 1
                time.sleep(2)
                
            except Exception as e:
                print(f"Error fetching movie list page {current_page}: {str(e)}")
                break

        movies_list = list(all_movies.values())
        result = sorted(movies_list[:50], key=lambda x: int(x.get('rank', '0')))
        print(f"\nFinal number of movies: {len(result)}")
        return result

    def get_movies_list(self, max_retries=5):
        """영화진흥위원회 API에서 영화 목록 조회"""
        kobis_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json"
        
        # 현재 상영중이거나 최근 개봉한 영화 위주로 검색
        today = datetime.now()
        target_date = (today - timedelta(days=30)).strftime('%Y%m%d')
        
        params = {
            'key': self.kobis_key,
            'openStartDt': target_date,  # 개봉 시작일
            'itemPerPage': 50  # 한 번에 가져올 영화 수
        }
        
        try:
            response = requests.get(kobis_url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return data.get('movieListResult', {}).get('movieList', [])
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch movies list: {str(e)}")
            return []
        

    def get_movie_details_from_kobis(self, movie_cd, max_retries=3):
        """영화진흥위원회 API에서 영화 상세정보 조회"""
        kobis_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json"
        params = {
            'key': self.kobis_key,
            'movieCd': movie_cd
        }
        
        for attempt in range(max_retries):
            try:
                response = requests.get(kobis_url, params=params, timeout=self.timeout)
                response.raise_for_status()
                movie_data = response.json()
                return movie_data.get('movieInfoResult', {}).get('movieInfo', {})
            except requests.exceptions.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed for KOBIS movie {movie_cd}: {str(e)}")
                if attempt == max_retries - 1:
                    logger.error(f"Failed to fetch KOBIS movie details after {max_retries} attempts")
                    return {}
                time.sleep(2 * (attempt + 1))

    def get_movie_details_from_kmdb(self, movie_title, directors=None, opendt=None, max_retries=3):
        """
        KMDB API에서 영화 상세정보 조회
        
        Args:
            movie_title (str): 영화 제목
            directors (list): 감독 이름 리스트
            opendt (str): 개봉일 (YYYY-MM-DD 형식)
        """
        kmdb_url = "http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp"
        
        params = {
            'ServiceKey': self.kmdb_key,
            'collection': 'kmdb_new2',
            'title': movie_title,
            'detail': 'Y'
        }
        
        if opendt:
            params['releaseDts'] = opendt.replace('-', '')
            
        for attempt in range(max_retries):
            try:
                response = requests.get(kmdb_url, params=params, timeout=self.timeout)
                response.raise_for_status()
                results = response.json().get('Data', [{}])[0].get('Result', [])
                
                if not results:
                    logger.warning(f"No KMDB results found for {movie_title}")
                    return {}
                    
                best_match = self._find_best_match(results, movie_title, directors, opendt)
                return self._extract_movie_details(best_match)
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed for KMDB movie {movie_title}: {str(e)}")
                if attempt == max_retries - 1:
                    logger.error(f"Failed to fetch KMDB details after {max_retries} attempts")
                    return {}
                time.sleep(2 * (attempt + 1))
            
    def _find_best_match(self, results, movie_title, directors, opendt):
        """결과 중 가장 적절한 항목 찾기"""
        best_match = None
        highest_match_score = 0
        
        for result in results:
            match_score = 0
            
            if movie_title == result.get('title'):
                match_score += 3
                
            if directors and result.get('directors'):
                kmdb_directors = [d.get('directorNm') for d in result['directors'].get('director', [])]
                if any(d in kmdb_directors for d in directors):
                    match_score += 2
                    
            if opendt and result.get('releaseDts'):
                if opendt.replace('-', '') == result['releaseDts']:
                    match_score += 2
                    
            if match_score > highest_match_score:
                highest_match_score = match_score
                best_match = result
                
        return best_match or results[0]
        
    def _extract_movie_details(self, movie_data):
        """영화 상세 정보 추출"""
        return {
            'director': ', '.join(d.get('directorNm', '') for d in movie_data.get('directors', {}).get('director', [])),
            'genre': movie_data.get('genre', ''),
            'poster_url': movie_data.get('posters', '').split('|')[0],
            'plot': movie_data.get('plots', {}).get('plot', [{}])[0].get('plotText', ''),
            'actors': ', '.join(a.get('actorNm', '') for a in movie_data.get('actors', {}).get('actor', [])[:5]),
            'nation': movie_data.get('nation', ''),
            'rating': movie_data.get('rating', '')
        }

    def create_fixtures(self):
        """영화 데이터를 수집하여 fixtures 파일 생성"""
        fixtures_data = []
        
        try:
            boxoffice_list = self.get_weekly_boxoffice()
            logger.info(f"Successfully fetched {len(boxoffice_list)} movies from weekly boxoffice")
            
            for index, movie in enumerate(boxoffice_list, start=1):
                logger.info(f"Processing ({index}/{len(boxoffice_list)}): {movie['movieNm']}")
                time.sleep(1)  # API 요청 간격 증가
                
                kobis_details = self.get_movie_details_from_kobis(movie['movieCd'])
                directors = [director['peopleNm'] for director in kobis_details.get('directors', [])]
                
                movie_details = self.get_movie_details_from_kmdb(
                    movie_title=movie['movieNm'],
                    directors=directors,
                    opendt=kobis_details.get('openDt')
                )
                
                try:
                    audience_acc = int(movie.get('audiAcc', 0))
                except (ValueError, TypeError):
                    audience_acc = 0
                    
                fixture = {
                    "model": "movies.movie",  # 앱 이름이 'movies'임을 반영
                    "pk": index,
                    "fields": {
                        "rank": int(movie.get('rank', 0)),
                        "title": movie.get('movieNm', ''),
                        "audience_acc": audience_acc,
                        "director": movie_details.get('director', ''),
                        "genre": movie_details.get('genre', ''),
                        "poster_url": movie_details.get('poster_url', ''),
                        "plot": movie_details.get('plot', ''),
                        "actors": movie_details.get('actors', ''),
                        "open_year": kobis_details.get('openDt', '')[:4],
                        "nation": movie_details.get('nation', ''),
                        "rating": movie_details.get('rating', ''),
                        "created_at": datetime.now().strftime('%Y-%m-%d')
                    }
                }
                
                fixtures_data.append(fixture)
            
            # fixtures 파일 저장
            fixtures_path = Path('movies/fixtures/boxoffice.json')  # 앱 이름이 'movies'임을 반영
            fixtures_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(fixtures_path, 'w', encoding='utf-8') as f:
                json.dump(fixtures_data, f, indent=4, ensure_ascii=False)
            
            logger.info(f"Successfully created fixtures for {len(fixtures_data)} movies")
            return fixtures_data
            
        except Exception as e:
            logger.error(f"Failed to create fixtures: {str(e)}")
            raise