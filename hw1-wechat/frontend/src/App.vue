<template>
  <div id="app">
    <div v-if="!authenticated">
      <ul class="nav nav-tabs">
        <li class="nav-item">
          <a class="nav-link active" href="#login">Login</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#register">Register</a>
        </li>
      </ul>

      <Login id="login" v-on:authenticated="setAuthenticated" />
      <Register
        id="register"
        :pics="profile_pics"
        v-on:authenticated="setAuthenticated"
      />
    </div>
    <b-container v-if="authenticated">
      <button type="button" @click="logout" class="btn btn-outline-danger">
        登出用户
      </button>

      <NavBar
        :logged_user="logged_user_username"
        :avatar="avatar"
        :cur_user="logged_user_id"
        :friends="friends"
      />
      <b-row class="main-area">
        <b-col v-if="on_chat" cols="4" class="users">
          <Groups
            :groups="groups"
            v-on:chat="chat"
            :profile_pics="profile_pics"
          />
        </b-col>
        <b-col v-else cols="4" class="users">
          <Users
            :pendings="pending_reqs"
            :users="friends"
            v-on:confMsg="send_message"
            :cur_user="logged_user_id"
            :profile_pics="profile_pics"
          />
        </b-col>
        <b-col cols="8" class="messages-area">
          <div class="messages-main">
            <div v-if="!current_chat_channel" class="select-chat text-center">
              Select a user to start chatting...
            </div>
            <Messages
              v-else
              :active_chat="logged_user_id"
              :messages="messages"
            />
          </div>
          <MessageInput v-on:send_message="send_message" />
        </b-col>
        <b-col cols="4">
          <TabBar
            v-on:switchTab="switchTab"
            :friendcnts="pending_reqs.length"
          ></TabBar>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script src="https://cdn.staticfile.org/axios/0.18.0/axios.min.js"></script>

<script>
import Vue from "vue";
import SocketIO from "socket.io-client";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
import NavBar from "./components/NavBar.vue";

import MessageInput from "./components/MessageInput.vue";
import Messages from "./components/Messages.vue";
import Login from "./components/Login.vue";
import Users from "./components/Users.vue";
import Groups from "./components/Chats.vue";


import Register from "./components/Register.vue";
import TabBar from "./components/Tabbar.vue";

export default {
  name: "app",
  components: {
    MessageInput,
    NavBar,
    Messages,
    Users,
    Login,
    Register,
    TabBar,
    Groups
  },
  data: function() {
    return {
      messages: {},
      message: "",
      avatar: "",
      friends: [],
      active_chat_id: null,
      active_chat_index: null,
      on_chat: true, //下方tabbar 助手，用于判断是否切换到聊天界面还是好友界面
      logged_user_id: null,
      logged_user_username: null,
      socket: SocketIO("http://localhost:5000/"),
      groups: [],
      authenticated: false,
      profile_pics: [],
      pending_reqs: [],
      current_chat_channel: null,
      activeUser: "",
      login_status: null,
      user_data: null
    };
  },
  created() {
    //注册界面提供所需要的头像
    this.axios.get(`http://localhost:5000/api/profiles`).then(response => {
      console.log(response.data);

      this.profile_pics = response.data;
    });
  },

  mounted() {
    this.refreshpage(); //刷新
    this.$root.$on("refreshpage", () => {
      this.refreshpage();
    });
    //监听套接字是否有新的信息
    this.socket.on("RESPONSE", data => {
      this.messages = data;
    });
  },
  methods: {
    async setAuthenticated(login_status, user_data) { //登录后获得所有相关信息
      //缓冲登录状态
      sessionStorage.setItem("login_status", login_status);
      sessionStorage.setItem("id", user_data.id);
      sessionStorage.setItem("username", user_data.username);
      sessionStorage.setItem("token", user_data.token);
      sessionStorage.setItem("avatar", user_data.avatar);

      // Update the states
      this.logged_user_id = user_data.id;
      this.logged_user_username = user_data.username;
      this.authenticated = login_status;
      this.token = user_data.token;
      this.avatar = this.profile_pics[user_data.avatar - 1].avat_dat;

      // 获取所有好友信息，
      let friends = await this.axios.get(
        `http://localhost:5000/api/friends/${user_data.id}`,
        {
          headers: { Authorization: "Bearer " + this.token }
        }
      );
      //查看是否有还有申请
      this.axios
        .get(`http://localhost:5000/api/friendpends/${this.logged_user_id}`)
        .then(response => {
          console.log(response);

          let req_data = response.data;
          // 把avatarid 转换为base64图片
          for (let j = 0; j < req_data.length; j++)
            req_data[j].avatar = this.profile_pics[
              req_data[j].avatar - 1
            ].avat_dat;

          console.log(req_data);

          this.pending_reqs = req_data;
        });

      // Get all users excluding the current logged user
      this.friends = friends.data.filter(
        user => user.userName != user_data.username
      );

      let friends_dat = friends.data;
      for (let j = 0; j < friends_dat.length; j++)
        friends_dat[j].avatar = this.profile_pics[
          friends_dat[j].avatar - 1
        ].avat_dat;

      console.log(friends_dat);

      this.friends = friends_dat;

      // 获取所有群聊，
      const groups = await this.axios.get(
        `http://localhost:5000/api/groups/${user_data.id}`,
        {
          headers: { Authorization: "Bearer " + this.token }
        }
      );
      this.groups = groups.data;

      for (let i = 0; i < this.groups.length; i++) {
        let avatar_list = this.groups[i].avatar;
        for (let j = 0; j < avatar_list.length; j++)
          this.groups[i].avatar[j] = this.profile_pics[
            this.groups[i].avatar[j] - 1
          ].avat_dat;
      }
      console.log(this.groups);

      //console.log(this.groups);
    },
    //页面刷新更新数据逻辑，重新请求数据库
    refreshpage() {
      let login_status = sessionStorage.getItem("login_status");
      let uname = sessionStorage.getItem("username");
      let id = sessionStorage.getItem("id");
      let token = sessionStorage.getItem("token");
      let avatar = sessionStorage.getItem("avatar");
      let userdata = {
        username: uname,
        id: id,
        token: token,
        avatar: avatar
      };
      this.axios.get(`http://localhost:5000/api/profiles`).then(response => {
        console.log(response.data);

        this.profile_pics = response.data;
        this.setAuthenticated(login_status, userdata);
      });
    },

    request_chat(id) {
      this.active_chat_id = id;
      this.active_chat_index = this.groups.findIndex( //查看当前聊天的好友下表
        user => user.group_id === this.active_chat_id
      );

      this.current_chat_channel = id;

      this.getMessage(id);
    },
    switchTab(id) { 
      if (id) this.on_chat = true;
      else this.on_chat = false;
    },
    chat_single(id) {},
    chat(id) {
      this.activeUser = id;
      console.log(id);
      this.request_chat(id);
    },

    date() { //转换timestamp
      const today = new Date();
      const date = `${today.getFullYear()}-${today.getMonth() +
        1}-${today.getDate()}`;
      const time = `${today.getHours()}:${today.getMinutes()}:${today.getSeconds()}`;
      const dateTime = `${date} ${time}`;
      // this.timestamp = dateTime;
      return dateTime;
    },

    send_message(message, type = 0) {
      console.log(type);
      console.log(message);
      if (type) { //发送图片或者文件

        this.socket.emit("event", {
          from_user: this.logged_user_id,
          to_group: this.active_chat_id,
          message: message,
          timestamp: this.date(),
          file: type
        });
      } else { //普通文字
        this.socket.emit("event", {
          from_user: this.logged_user_id,
          to_group: this.active_chat_id,
          message: message,
          timestamp: this.date(),
          file: type
        });
        this.message = "";
      }
    },

    logout() {
      sessionStorage.removeItem("login_status");
      sessionStorage.removeItem("username");
      sessionStorage.removeItem("id");
      sessionStorage.removeItem("token");
      sessionStorage.removeItem("avatar");

      this.authenticated = false;
    },
    getMessage: function(group_id) { //获得该聊天群的所有信息
      this.axios
        .get(`http://localhost:5000/api/get_message/${group_id}`, {
          headers: { Authorization: "Bearer " + this.token }
        })
        .then(response => {
          this.messages = [];
          for (let i = 0; i < response.data.length; i++) {
            this.messages.push(response.data[i]);
          }
          console.log(this.messages);
        });
    }
  }
};
</script>

<style>
@import url("./assets/base.css");

#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.messages-main {
  overflow-y: scroll;
  height: 90%;
}
.users {
  padding: 0px !important;
  border: 1px solid gray;
}
.no-margin {
  margin: 0px;
}
.messages-area {
  border: 1px solid gray;
  padding: 0px !important;
  max-height: calc(100vh - 4em) !important;
}
.input-message {
  height: 40px;
}

.select-chat {
  margin-top: 35vh;
  padding: 8px;
}
.main-area {
  margin: 0px;
  min-height: calc(100vh - 5em) !important;
}
.logged_user {
  color: white;
}
</style>
