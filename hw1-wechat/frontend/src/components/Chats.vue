<template>
  <div style="margin-top: 0px;">
    <b-list-group style="" v-for="(group, id) in groups" v-bind:key="id">
      <b-list-group-item
        class="d-flex align-items-center"
        v-bind:class="[
          activeGroup == group.group_id ? 'group active' : 'group'
        ]"
        v-on:click="chat(group.group_id)"
      >
        <b-avatar-group style="width:100px;"
          size="30px"
          v-for="avat in group.avatar"
          v-bind:key="avat"
          overlap="0.5"
        >
          <b-avatar :src="'data:image/png;base64,' + avat"></b-avatar>
        </b-avatar-group>

        <span class="mr-auto">{{ group.groupname }}</span>
        <span v-if="group.has_new_message" class="has_new_message"
          >New message</span
        >
      </b-list-group-item>
    </b-list-group>
  </div>
</template>
<script>
export default {
  name: "Groups",
  props: {
    groups: Array
  },
  data() {
    return {
      activeGroup: null
    };
  },
  methods: {
    chat: function(id) {
      this.activeGroup = id;
      this.$emit("chat", id);
    }
  }
};
</script>
<style scoped>
.group {
  margin: 0px ;
  padding: 10px 4px 10px 8px;
  border-bottom: 1px solid gray;
}
.active {
  background: #17a2b8;
  color: white;
}
.has_new_message {
  background-color: #57973a;
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
