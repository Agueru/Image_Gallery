<script setup>
import { onMounted } from 'vue';
import api from '../api';
import { useStore } from 'vuex';

const store = useStore();

onMounted(() => {
  const sortOrder = localStorage.getItem("sortOrder");
  
  if (store.state.user) {
    api.get(`/users/${store.state.user.user_id}/images`).then(response => {
      store.commit("setImages", {images: [...response.data], order: sortOrder})
    });
  }
  else {
    api.get(`/images`).then(response => {
      
      store.commit("setImages",  {images: [...response.data], order: sortOrder})
    });
  }

});
</script>


<template>
  <div class="container">
    <h1 class="text-center mb-4">Image Gallery</h1>
    <div class="d-flex align-items-center justify-content-between sort-bar my-2">
      <span class="text-white">Sort by date:</span>
      <div class="btn-group" role="group">
        <button type="button" class="btn btn-dark mx-1" @click="sortAscending">Ascending</button>
        <button type="button" class="btn btn-dark mx-1" @click="sortDescending">Descending</button>
      </div>
    </div>
    <div class="row">
      <div v-for="(image, index) in $store.state.images" :key="index" class="col-md-4">
        <div class="card mb-4">
          <img :src="image.url" class="card-img-top" alt="Image" @click="openImageModal(index)">
          <div class="card-body">
            <div class="d-flex align-items-center justify-content-between">
              <h5 class="card-title">{{ image.title }}</h5>
              <div v-if="$store.state.user?.user_id && $store.state.user.user_id === image.user_id">
                <button class="btn btn-outline-danger" @click="deleteImage(image.id)">x</button>
              </div>
              <div v-else>
                <span class="username">{{ image.user_name }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <ImageModal :image="selectedImage" :visible="modalVisible" @close="closeImageModal" v-if="selectedImage" />
  </div>
</template>

<script>
import ImageModal from './ImageModal.vue';

export default {
  name: 'Home',
  components: {
    ImageModal,
  },
  data() {
    return {
      modalVisible: false,
      selectedImage: null,
    };
  },
  methods: {
    sortAscending() {
      this.$store.commit('setOrder', 'ascending');
      localStorage.setItem('sortOrder', 'ascending');
    },
    sortDescending() {
      this.$store.commit('setOrder', 'descending');
      localStorage.setItem('sortOrder', 'descending');
    },
  deleteImage(imageId) {
    api.delete(`/users/${this.$store?.state?.user?.user_id}/images/${imageId}`)
      .then((response) => {
        if (response.status === 204) {
          this.$store.commit('removeImage', imageId);
        }
      });
    },
    openImageModal(index) {
      this.selectedImage = this.$store.state.images[index];
      this.modalVisible = true;
    },
    closeImageModal() {
      this.modalVisible = false;
    },
  },
};
</script>

<style scoped>
.card {
  width: fit-content;
  background-color: rgba(0, 0, 0, 0.3); 
}
img:hover {
  box-shadow: 0 0 2px 1px rgba(0, 140, 186, 0.5);
  opacity: 0.7;
  cursor: pointer;
  transition: 0.3s;
}
.username {
  background-color: rgba(0, 0, 0, 0.3); 
  padding: 4px 8px;
  border-radius: 4px; 
  color: white;
  font-weight: bold; 
  position: absolute;
  top: 5px;
  right: 5px;
  
  
}
.card-title {
  background-color: rgba(0, 0, 0, 0.3); 
  padding: 4px 8px;
  border-radius: 4px;  
  color: white;
}

.card img {
  height: 250px;
  object-fit: cover;
}

@media (max-width: 768px) {
  .card {
    width: 100%;
  }
}
</style>
