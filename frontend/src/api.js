import axios from "axios";
import { useStore } from "vuex";
import { toast } from "vue3-toastify";
import jwtDecode from "jwt-decode";

const store = useStore();
const api = axios.create({
  baseURL: "http://localhost:5000/api/v1",
});

let subscribers = [];

function subscribeTokenRefresh(callback) {
  subscribers.push(callback);
}

api.interceptors.request.use(
  async (config) => {
    const token = localStorage.getItem("token");

    if (token) {
      const decodedToken = jwtDecode(token);
      const currentTime = Date.now() / 1000;

      if (decodedToken.exp < currentTime) {
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        store.commit("setUserLoggedOut");
        window.location.href = "/login";
        toast("Your session has expired. Please login again.", {
          type: "error",
        });

        return new Promise((resolve) => {
          subscribeTokenRefresh((token) => {
            config.headers.Authorization = `Bearer ${token}`;
            resolve(config);
          });
        });
      } else {
        config.headers.Authorization = `Bearer ${token}`;
        return config;
      }
    } else {
      if (store) {
        store.commit("setUserLoggedOut");
      }
      return config;
    }
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    if (error.response.status === 401 && !originalRequest._retry) {
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      store.commit("setUserLoggedOut");
      window.location.href = "/login";
      toast("Your session has expired. Please login again.", {
        type: "error",
      });

      return new Promise((resolve) => {
        subscribeTokenRefresh((token) => {
          originalRequest.headers.Authorization = `Bearer ${token}`;
          originalRequest._retry = true;
          resolve(axios(originalRequest));
        });
      });
    }

    return Promise.reject(error);
  }
);

export default api;
