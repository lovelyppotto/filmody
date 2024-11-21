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
import LibraryView from "@/views/LibraryView.vue";
import MovieDetailView from "@/views/MovieDetailView.vue";


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
      path: "/movies/:id",
      name: 'movieDetail',
      component: MovieDetailView,
    },
    {
      path: '/playlist',
      name: 'PlaylistView',
      component: PlaylistView,
    },
    {
      path:'/library',
      name: 'LibraryView',
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
    // {
    //   path: '/playlist/:id/videos',
    //   name: 'PlaylistVideos',
    //   component: 
    // },
  ],
});

export default router;
