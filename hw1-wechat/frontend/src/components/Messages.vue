<template>
  <div>
    <b-container class="bv-example-row mb-3">
      <div v-for="message in messages" v-bind:key="message.id">
        <b-row
          align-v="end"
          class="col-md-5"
          cols="4"
          v-bind:class="[
            message.from_user == active_chat
              ? 'offset-md-7 justify-content-end'
              : 'justify-content-end flex-row-reverse'
          ]"
        >
          <b-col
            ><span class="Username">{{ message.from_username }}</span></b-col
          >
          <b-col
            ><b-avatar
              size="40px"
              :src="'data:image/png;base64,' + message.avatar"
            >
            </b-avatar
          ></b-col>
        </b-row>
        <b-row
          v-bind:class="[
            message.from_user == active_chat
              ? 'offset-md-7 justify-content-end'
              : 'justify-content-start'
          ]"
        >
          <b-col cols="10"
            ><span class="timestamp">{{ message.time }}</span></b-col
          >
        </b-row>
        <b-row>
          <div
            class="chat-message col-md-5"
            v-if="!message.file"
            v-bind:class="[
              message.from_user == active_chat
                ? 'from-message offset-md-6'
                : 'to-message offset-md-1'
            ]"
          >
            {{ message.message }}
          </div>
          <div
            v-else
            class="chat-message col-md-5"
            v-bind:class="[
              message.from_user == active_chat
                ? 'from-message offset-md-6'
                : 'to-message offset-md-1'
            ]"
          >
            <img class="img-thumbnail" :src="'data:image/png;base64,' + message.message" />
          </div>
        </b-row>
      </div>
    </b-container>
  </div>
</template>
<script>
export default {
  name: "Messages",
  props: {
    messages: Array,
    active_chat: Number,
    profile_pics: Array
  },
  mounted() {}
};
</script>
<style>
.from-message_avat {
  color: white;
  margin-bottom: 4px;
}
.from-message {
  background: #2ea842;
  color: white;
  border-radius: 3px;
  padding: 8px 2px;
  margin-bottom: 4px;
}
.to-message {
  background: rgb(201, 209, 209);
  color: rgb(41, 53, 52);
  border-radius: 3px;
  padding: 8px 2px;
  margin-bottom: 4px;
}
.to-message_avat {
  color: rgb(41, 53, 52);
  margin-bottom: 4px;
}
.timestamp {
  font-size: 7px;
  color: gray;
}
.Username {
  font: size 12px;
  color: rgb(53, 50, 50);
}
</style>
