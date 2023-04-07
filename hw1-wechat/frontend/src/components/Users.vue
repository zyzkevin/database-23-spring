<template>
  <div style="margin-top: 0px; b- q">
    <b-list-group v-for="user in users" v-bind:key="user.id">
      <b-list-group-item
        class="d-flex align-items-center"
        v-bind:class="[activeUser == user.user_id ? 'user' : 'user']"
        v-on:click="chat(user.user_id)"
      >
        <b-avatar :src="'data:image/png;base64,' + user.avatar"></b-avatar>

        <span class="mr-auto">{{ user.userName }}</span>
      </b-list-group-item>
    </b-list-group>

    <b-list-group v-for="user in pendings" v-bind:key="user.id">
      <b-list-group-item
        class="d-flex align-items-center"
        v-bind:class="[activeUser == user.user_id ? 'user' : 'user']"  
        v-on:click="chat(user.id)"
      >
        <b-avatar :src="'data:image/png;base64,' + user.avatar"></b-avatar>

        <span class="mr-auto">{{ user.userName }}</span>

        <button @click="acceptreq(user)" class="btn">
          <b-icon  icon="check"></b-icon>
          接受邀请
        </button>
      </b-list-group-item>
    </b-list-group>
  </div>
</template>
<script>
export default {
  name: "Users",
  props: {
    users: Array,
    cur_user: Number,
    pendings: Array
  },
  data() {
    return {
      activeUser: null
    };
  },
  methods: {
    chat: function(id) {
      this.activeUser = id;
      this.$emit("chat", id);
    },
    acceptreq: function(user) { //确认好友申请
      const AxiosObj = this.axios;

      const details = {
        from_user: user.id,
        to_user: this.cur_user
      };
      const group_details = {
          group_mems: [details.from_user, details.to_user],
          group_name: user.userName
        };

        //第一发出好友确认请求，双方都成为好友
      this.axios
        .post("http://localhost:5000/api/confirmFriend", details)
        .then(response => {
          
          console.log(group_details);
          //创建新的聊天进程
          this.createGroup(group_details);

          alert(response.data.message);
          // if (response.data.status === 'success') {
          //after adding friend, now create new group

          this.$root.$emit('refreshpage');

        });
    },
    createGroup(group_details) {
      const that = this;
      console.log(group_details);
      this.axios
            .post("http://localhost:5000/api/createGroup", group_details)
            .then(response => {
                this.$root.$emit("refreshpage");
              alert(response.data.message);
              //after creating tgroup, now send msg!
            });
          //after creating group, now send msg!
          // }
    }
  }
};
</script>
<style scoped>
.user {
  margin: 0px ;
  padding: 10px 4px 10px 8px;
  border-bottom: 1px solid gray;
}
.active {
  background: #17a2b8;
  color: white;
}
.has_new_message {
  background-color: #17a2b8;
  border-radius: 4px;
  display: inline-block;
  color: white;
  margin-bottom: -4px;
  font-size: 10px;
  margin: 4px;
  padding: 3px;
  font-weight: bolder;
}
</style>
