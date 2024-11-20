import HomeView from "@/views/HomeView.vue";
import MovieDetailView from "@/views/MovieDetailView.vue";
import MovieListView from "@/views/MovieListView.vue";
import ReviewSearchView from "@/views/ReviewSearchView.vue";
import { createRouter, createWebHistory } from "vue-router";
import SignUpView from "@/views/SignUpView.vue";
import LogInView from "@/views/LogInView.vue";
import ProfileView from "@/views/ProfileView.vue";
import MovieSearchView from "@/views/MovieSearchView.vue";
import PlaylistView from "@/views/PlaylistView.vue";
import PlaylistDetail from "@/views/PlaylistDetail.vue";
import RecommendView from "@/views/RecommendView.vue";


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "HomeView",
      component: HomeView,
    },
    {
      path: '/signup',
      name: 'SignUpView',
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
      path: "/movies",
      name: "MovieListView",
      component: MovieListView,
    },
    {
      path: "/:movieId",
      name: "MovieDetailView",
      component: MovieDetailView,
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
      path: '/playlist/:id',
      name: 'playlist-detail',
      component: PlaylistDetail,
    }
  ],
});

export default router;
