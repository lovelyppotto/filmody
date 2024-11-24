import HomeView from "@/views/HomeView.vue";
import ReviewSearchView from "@/views/ReviewSearchView.vue";
import { createRouter, createWebHistory } from "vue-router";
import SignUpView from "@/views/SignUpView.vue";
import LogInView from "@/views/LogInView.vue";
import ProfileView from "@/views/ProfileView.vue";
import MovieSearchView from "@/views/MovieSearchView.vue";
import PlaylistView from "@/views/PlaylistView.vue";
import PlaylistDetail from "@/views/PlaylistDetail.vue";
import RecommendView from "@/views/RecommendView.vue";
import CreatePlaylistModal from "@/components/Playlist/CreatePlaylistModal.vue";
import LibraryView from "@/views/LibraryView.vue";
import MovieDetailView from "@/views/MovieDetailView.vue";
import LikedPlaylistView from "@/views/LikedPlaylistView.vue";
import MyPlaylistView from "@/views/MyPlaylistView.vue";
import UserProfile from "@/views/UserProfile.vue";


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView
    },
    {
      path: '/login',
      name: 'LogInView',
      component: LogInView
    },
    {
      path: '/profile/:username',
      name:'ProfileView',
      component: ProfileView
    },
    {
      path: "/movies/search",
      name: "MovieSearchView",
      component: MovieSearchView,
    },
    {
      path: "/movies/:id",
      name: 'movieDetail',
      component: MovieDetailView,
    },
    {
      path: "/movies/library",
      name: 'library-movie',
      component: MovieDetailView,
    },
    {
      path: "/review-search",
      name: "ReviewSearchView",
      component: ReviewSearchView,
    },
    {
      path: "/recommend",
      name: "Recommend",
      component: RecommendView,
    },
    {
      path: '/playlist',
      name: 'PlaylistView',
      component: PlaylistView,
    },
    {
      path:'/library/movies',
      name: 'LikedMovies',
      component: LibraryView,
    },
    {
      path: '/playlist/:id',
      name: 'playlist-detail',
      component: PlaylistDetail,
      children: [
        {
          path: 'reviews',
          name: 'PlaylistReviews',
          component: () => import('@/components/PlaylistReviews/PlaylistReviewList.vue')
      }
      ]
    },
    {
      path: '/playlist/:id',
      name: 'playlist-detail',
      component: () => import('../views/PlaylistDetail.vue'),
      children: [
        {
          path: 'videos',  // /playlist/:id/videos
          name: 'playlist-videos',
          component: () => import('@/components/Playlist/PlaylistVideo.vue')
        }
      ]
    },
    {
      path: '/playlist/create',
    name: 'playlist-create',
    component: CreatePlaylistModal,  // CreatePlaylist 컴포넌트를 연결
    }, 
    {
      path: '/playlist/liked-playlist',
      name: 'liked-playlists',
      component: LikedPlaylistView
    },
    {
      path: '/playlist/my-playlist',
      name: 'my-playlists',
      component: MyPlaylistView
    },
    {
      path:'/users/:id',
      name: 'UserProfile',
      component:UserProfile
    },
    {
      path:'/users/:id/followers',
      name: 'UserFollowers',
      component:UserProfile
    },
    {
      path:'/users/:id/following',
      name: 'UserFollowing',
      component:UserProfile
    },
    
  ],
});

export default router;
