<template>
  <b-navbar
    toggleable="md"
    type="dark"
    variant="info"
    class="navbar navbar-dark bg-dark"
  >
    <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
    <b-navbar-brand href="#">我的微信</b-navbar-brand>

    <b-collapse is-nav id="nav_collapse">
      <b-dropdown no-caret>
        <template #button-content>
          添加好友或创建新群
          <b-icon icon="plus-square"></b-icon>
        </template>

        <b-dropdown-item v-b-modal.add_friend>添加好友</b-dropdown-item>
        <b-dropdown-item v-b-modal.addGroup>发起群聊</b-dropdown-item>
      </b-dropdown>

      <b-modal
        id="addGroup"
        title="创建新群聊"
        @show="resetModal"
        @hidden="resetModal"
        @ok="handleGroup"
      >
        <form id="form_group" ref="form_group" @submit.stop.prevent="addGroup">
          <b-form-group>
            <b-form-checkbox
              v-for="user in friends"
              :key="user.id"
              v-model="user.checked"
              class="d-flex align-items-center"
            >
              <b-avatar
                :src="'data:image/png;base64,' + user.avatar"
              ></b-avatar>

              <span class="mr-auto">{{ user.userName }}</span>
            </b-form-checkbox>
          </b-form-group>

          <b-form-group
            label="输入群名"
            label-for="name-input"
            invalid-feedback="Name is required"
          >
            <b-form-input
              id="name-input"
              v-model="groupname"
              required
            ></b-form-input>
          </b-form-group>
        </form>
      </b-modal>

      <b-modal
        id="add_friend"
        title="添加好友"
        @show="resetModal"
        @hidden="resetModal"
        @ok="handleOk"
      >
        <form ref="form" @submit.stop.prevent="addFriend">
          <b-form-group
            label="请输入对方用户名"
            label-for="name-input"
            invalid-feedback="Name is required"
          >
            <b-form-input id="name-input" v-model="fid" required></b-form-input>
          </b-form-group>
        </form>
      </b-modal>
      <b-avatar :src="'data:image/png;base64,' + avatar"> </b-avatar>
      <b-navbar-nav class="ml-auto logged_user">
        欢迎回来！ {{ logged_user }}
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
export default {
  data() {
    return {
      fid: "",
      activeUser: "",
      groupname: ""
    };
  },
  name: "NavBar",
  props: {
    logged_user: String,
    avatar: String,
    cur_user: Number,
    friends: Array
  },
  methods: {
    resetModal() {
      this.fid = "";
    },
    handleOk(bvModalEvent) {
      // 
      this.addFriend();
    },

    handleGroup(bvModalEvent) {
      //所有选中用户创建群
      let checked_users = this.friends
        .filter(user => user.checked)
        .map(user => user.id);
      console.log(checked_users);

      const group_details = {
        group_mems: [this.cur_user].concat(checked_users),
        group_name: this.groupname
      };

      console.log(group_details);

      this.createGroup(group_details);
    },

    addFriend: function() { //添加好友
      const details = {
        from_user: this.cur_user,
        to_user: this.fid
      };
      console.log(details);
      this.axios
        .post("http://localhost:5000/api/addfriend", details)
        .then(response => {
          alert(response.data.message);

        })
        .catch(response => {
          alert(response.data.message);
        });

      this.$nextTick(() => {
        this.$bvModal.hide("modal-prevent-closing");
      });
    },

    addGroup(e) {
      console.log(e);
    },

    createGroup: function(group_details) {
      this.axios
        .post("http://localhost:5000/api/createGroup", group_details)
        .then(response => {
          this.$nextTick(() => {
            this.$bvModal.hide("modal-prevent-closing");
            this.$root.$emit("refreshpage");
          });
          //after creating tgroup, now send msg!
          //this.$emit("confMsg", "我们已经成为好友，现在可以开始聊天了！");
        });
      //after creating group, now send msg!
      // }
    }
  },
  mounted() {
    //用
  }
};
</script>

<style scoped>
.nav-bar {
  border-bottom: 1px solid #40793e;
}
</style>
