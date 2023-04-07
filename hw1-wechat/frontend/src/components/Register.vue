<template>

<div class="col-md-12">


  <div class="card card-container">
    <h4></h4>

    <form @submit.prevent="register">
      <div class="form-group">
        <label for="username">Username</label>
        <div>
        <input id="username" type="type" v-model="username"  rules="rules.username" class="form-control" required autofocus />
        </div>
      </div>
     
      <div class="form-group">
        <label for="password">Password</label>
       <div>
          <input  name="password" id="password" type="password"  class="form-control" v-model="password" required />
        </div>
      </div>
      <div class="form-group">
        <label for="password">Confirm Password</label>
       <div>
          <input name="cpassword" id="cpassword" type="password" v-model="cpassword"  class="form-control" required />
        </div>
      </div>

      <div v-for="(pic, id) in pics" v-bind:key="id"  id="profileselection" class="d-flex p-2 flex-row justify-content-around">
        <div v-bind:class="[avatar == id ? 'profactive': '']" v-on:click ="imgSel(id)">
            <img :src= "'data:image/png;base64,' + pic.avat_dat" />
        </div>
      </div>

      <div class="form-group">
     <!-- this is where we call the login function -->
      <button class="btn btn-primary btn-block" :disabled="loading">
            <span v-show="loading" class="spinner-border spinner-border-sm"></span>
            <span>Register</span>
          </button>
      </div>
      <div>
        <button class="but" type="button" onclick="window.location.href = '#login';">Login</button>
      </div>

      
    </form>
  </div>
  </div>
</template>
<script>
import { required, sameAs, minLength } from "vuelidate/lib/validators";
import router from "../router";

export default {
  name: "Register",
  props: {
    pics: Array,
  },
  data() {
    return {

      loading: false,
      email: "",
      username: "",
      password: "",
      cpassword: "",
      rules: {
        username: [
          (v) => !!v || "Username is required",
        ],
        password: [
          (v) => !!v || "Password is required",
        ],
      },
      avatar: 0, //default
      validations: {
        password: {
          required,
          minLength: minLength(3),
        },
        cpassword: {
          sameAsPassword: sameAs("password"),
        },
      },
      imgSel(id) {
        this.avatar = id;
      }
    };
  },
  methods: {
   
  },
  computed: {
    loggedIn() {
      return this.username;
    },
  },
  mounted() {
    
  },
  methods: {
    register() {
      const details = {
        username: this.username,
        password: this.password,
        cpassword: this.cpassword,
        avatar: this.avatar
      };
      this.axios
        .post("http://localhost:5000/api/signup", details)
        .then((response) => {
          alert(response.data.message);

        })
        .catch((response) => {
          alert(response.data.message);
        });
    },
  },
};
</script>
<style scoped>
label {
  display: block;
  margin-top: 10px;
}
#profileselection {
  width:100%;
}
#profileselection img{
  width: 90px;
  height: 90px;
}

.profactive {
  padding: 5px;
  border: 4px bold green;
  background: green;
}

.card-container.card {
  max-width: 350px;
  padding: 40px 40px;
}


.card {
  background-color: #f7f7f7;
  padding: 20px 25px 30px;
  margin: 0 auto 25px;
  margin-top: 50px;
  -moz-border-radius: 2px;
  -webkit-border-radius: 2px;
  border-radius: 2px;
  -moz-box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.3);
  -webkit-box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.3);
  box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.3);
}

.profile-img-card {
  width: 96px;
  height: 96px;
  margin: 0 auto 10px;
  display: block;
  -moz-border-radius: 50%;
  -webkit-border-radius: 50%;
  border-radius: 50%;
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