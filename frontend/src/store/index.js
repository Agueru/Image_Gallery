import { createStore } from "vuex";

const sortImages = (images, sortOrder) => {
  const sorted = images.sort((a, b) => {
    const dateA = Date.parse(a.uploaded_at);
    const dateB = Date.parse(b.uploaded_at);
    return sortOrder === "ascending" ? dateA - dateB : dateB - dateA;
  });
  return sorted;
};

const store = createStore({
  state() {
    return {
      user: null,
      isAuthenticated: false,
      images: [],
    };
  },
  mutations: {
    setUserLoggedIn(state, user) {
      state.user = user;
      state.isAuthenticated = true;
    },
    setUserLoggedOut(state) {
      state.user = null;
      state.isAuthenticated = false;
      state.images = [];
    },
    setImages(state, payload) {
      const { images, order } = payload;
      state.images = sortImages(images, order);
    },
    setOrder(state, sortOrder) {
      state.images = sortImages(state.images, sortOrder);
    },
    removeImage(state, imageId) {
      state.images = state.images.filter(img => img.id !== imageId);
    }
  }

});

export default store;
