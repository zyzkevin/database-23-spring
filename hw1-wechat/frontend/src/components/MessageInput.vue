<template>
  <div class="input_box">
    <div class="mb-3">
      <label for="formFile" class="form-label"></label>
      <input
        @change="uploadImage($event)"
        accept="image/*"
        class="form-control"
        type="file"
        id="formFile"
      />
    </div>

    <div class="message-input input-lg">
      <b-form-input
        v-model="message_input"
        type="text"
        placeholder="Enter your message"
        v-on:keyup.enter.native="send_message"
      >
      </b-form-input>
    </div>
  </div>
</template>

<script>
export default {
  name: "MessageInput",
  data() {
    return {
      message_input: ""
    };
  },
  
  methods: {
    send_message() {
      this.$emit("send_message", this.message_input, 0);
      this.message_input = "";
    },
    
    async uploadImage(event) {
      //把上传的图片转化为byte传给后端
      let file = event.currentTarget.files[0];
      const buffer = await file.arrayBuffer();
    
      let bytearray =null;
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
          bytearray = reader.result.split(',')[1];
          this.$emit("send_message", bytearray, 1);
          console.log(bytearray);
      };

      
    }
  }
};
</script>

<style scoped>
.input_box {
  position: relative;

  bottom: 0;
  width: 100%;
  height: 300px;
}
.message-input {
  bottom: 0;
  height: 200px;
  width: 100%;
}
</style>
