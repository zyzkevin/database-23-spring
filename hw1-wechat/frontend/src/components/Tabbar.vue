<template>
  <div class="main-tab-bar">
    <div id="tab-bar">
      <div
        class="tab-bar-item"
        v-on:click="switchTab(1)"
        path="/home"
        :class="[tabbar_id == 1 ? 'active' : '']"
      >
        <b-icon icon="chat-fill" v-if="tabbar_id==1"></b-icon>
        <b-icon icon="chat" v-if="tabbar_id == 0"></b-icon>

        <div>聊天</div>
      </div>
      <div
        class="tab-bar-item"
        v-on:click="switchTab(0)"
        :class="[tabbar_id == 0 ? 'active' : '']"
      >
        <b-icon icon="people-fill" v-if="tabbar_id == 0"></b-icon>
        <b-icon icon="people" v-if="tabbar_id == 1"></b-icon>

        <span>通讯录</span>
        <span class="text-center">
        <b-button variant="primary">
          新好友申请 <b-badge variant="light">{{friendcnts}}</b-badge>
        </b-button>
      </span>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "TabBar",
  data() {
    return {
      tabbar_id: 1
    };
  },
  props: {
    friendcnts: Number
  },
  methods: {
    switchTab(id) {
      this.tabbar_id = id;
      console.log(id);
      this.$emit("switchTab", this.tabbar_id);
    },
    isActive(id) {
      if (id == this.id) return true;
      else return false;
    }
  },

};
</script>
<style scoped>
.active {
  text-emphasis-color: rgb(78, 165, 51);
}
#tab-bar {
  display: flex;
  background-color: #f6f6f6;
  position: fixed;
  width: 50%;
  bottom: 0;
  box-shadow: 0 -1px 1px rgba(100, 100, 100, 0.2);
}

.tab-bar-item {
  flex: auto;
  text-align: center;
  height: 49px;
  font-size: 14px;
}
.tab-bar-item img {
  height: 24px;
  width: 24px;
  margin-top: 3px;
  vertical-align: middle;
  margin-bottom: 2px;
}
</style>
