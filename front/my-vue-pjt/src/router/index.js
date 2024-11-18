import HomeView from "@/views/HomeView.vue";
import MovieDetailView from "@/views/MovieDetailView.vue";
import MovieListView from "@/views/MovieListView.vue";
import ReviewSearchView from "@/views/ReviewSearchView.vue";
import { createRouter, createWebHistory } from "vue-router";
import RecommendedView from '@/views/RecommendedView.vue'  // 파일명 확인


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "HomeView",
      component: HomeView,
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
      path: "/review-search",
      name: "ReviewSearchView",
      component: ReviewSearchView,
    },
    {
      path: "/recommend",
      name: "recommend",
      component: RecommendedView,
    },
    {
      path: "/movies/:id",
      name: 'movieDetail',
      component: MovieDetailView,
    }
  ],
});

export default router;
