<template>
  <div class="container">
    <h1 class="text-center mb-4">Image Upload</h1>
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <form @submit.prevent="uploadImage">
              <div class="form-group my-2">
                <label for="title">Title</label>
                <input type="text" class="form-control" id="title" v-model="title" placeholder="Enter image title" required>
              </div>
              <div class="form-group my-2">
                <label for="image">Image</label>
                <input type="file" class="form-control-file d-block" id="image" @change="handleImageChange" required>
              </div>
              <button type="submit" class="btn btn-outline-dark my-3">Upload</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../api';
import { toast } from 'vue3-toastify';

export default {
  name: 'ImageUpload',
  data() {
    return {
      title: '',
      imageFile: null,
      inputTarget: null
    };
  },
  methods: {
    handleImageChange(event) {
      this.imageFile = event.target.files[0];
      this.inputTarget = event.target;
    },
    uploadImage() {
      const formData = new FormData();
      formData.append('title', this.title);
      formData.append('image', this.imageFile);

      api.post('/images/upload', formData)
        .then((response) => {
          response.status === 201 && toast('Image uploaded successfully', {
            type: 'success',
          })

         
          this.title = '';
          this.imageFile = null;
          if(this.inputTarget){
            this.inputTarget.value = null;
          }
        })
        .catch((error) => {
          console.log(error)
          toast('Something went wrong', {
            type: 'error',
          })
        });
    },
  },
};
</script>
