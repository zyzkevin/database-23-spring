<template>
    <div class="login">
      <div v-if="proccessing" class="text-center"> Please wait... </div>
      <div v-if="message" class="text-center"> {{message}} </div>
      
      <b-form-input
        v-model="username"
        type="text"
        class="input-form"
        placeholder="Username">
      </b-form-input>
      
      <b-form-input
        v-model="password"
        class="input-form"
        type="password"
        placeholder="Password">
      </b-form-input>
      
      <b-button 
        v-on:click="login" 
        variant="primary" 
        class="btn-block"
      >
      Log me in
     </b-button>
      <div>
        <button class="but" type="button" onclick="window.location.href = '#register';">Signup</button>
      </div>
    </div>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      username: "",
      password: "",
      proccessing: false,
      message: ""
    };
  },
  methods: {
    login: function() { //登录逻辑
      this.loading = true;
      this.axios
        .post("http://localhost:5000/api/login", {
          username: this.username,
          password: this.password
        })
        .then(response => {
          if (response.data.status == "success") {
            this.proccessing = false;
            this.$emit("authenticated", true, response.data.data);
            console.log(response.data.data);
          } else {
            this.message = "登录失败！";
          }
        })
        .catch(error => {
          console.log(error)

          this.message = "登录失败！";
          this.proccessing = false;
        });
    }
  }
};
</script>

<style scoped>
.login {
  width: 500px;
  border: 1px solid #cccccc;
  background-color: #ffffff;
  margin: auto;
  margin-top: 200px;
  padding: 20px;
}
.input-form {
  margin-bottom: 9px;
}
.but {
  border-radius: 4px;
  color: #1a73e8;
  display: inline-block;
  font-weight: 500;
  letter-spacing: 0.25px;
  background-color: transparent;
  border: 0;
  cursor: pointer;
  font-size: inherit;
  outline: 0;
  padding: 0;
  text-align: left;
}
</style>