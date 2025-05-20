<template>
  <div class="modal" v-if="visible">
    <div class="modal-content">
      <span class="close" @click="closeModal">&times;</span>
      <div class="user-name">{{ image.user_name }}</div>
      <img :src="image.url" alt="Image" class="modal-image">
    </div>
  </div>
</template>

<script>
export default {
  name: 'ImageModal',
  props: {
    image: {
      type: Object,
      required: true,
    },
    visible: {
      type: Boolean,
      required: true,
    },
  },
  methods: {
    closeModal() {
      this.$emit('close');
    },
  },
};
</script>

<style scoped>
.modal {
  display: block;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  bottom: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.5);

}

.modal-content {
  margin: 2% auto;
  background-color: transparent;
  padding: 1px;
  border-radius: 2%;
  position: relative;
  border: none;
}

.close {
  position: fixed;
  top: 5px;
  right: 20px;
  color: #f1f1f1;
  font-size: 40px;
  font-weight: bold;
  
}

.close:hover{
  color: #bbb;
  text-decoration: none;
  cursor: pointer;
}
.modal-image {
  max-width: 100%;
  max-height: 90vh;
  object-fit: contain;
  margin: auto;
  border-radius: 2%;
  animation-name: zoom;
  animation-duration: 0.6s;
  
}
@keyframes zoom {
  from {transform: scale(0.1)}
  to {transform: scale(1)}
}


.user-name {
  background-color: rgba(0, 0, 0, 0.3); 
  padding: 4px 8px;
  border-radius: 4px; 
  color: white;
  font-weight: bold; 
  margin: auto;
  display: block;
  width: 80%;
  max-width: 700px;
  text-align: center;
  padding: 10px 0;
  
}


.modal-image, .user-name {  
  animation-name: zoom;
  animation-duration: 0.6s;
  
}
</style>
