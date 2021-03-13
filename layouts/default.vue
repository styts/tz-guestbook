<template>
  <v-app dark>
    <v-app-bar fixed app>
      <v-toolbar-title>
        Tezos Guestbook
      </v-toolbar-title>
      <v-spacer />
      <span class="net">
        Edonet (testnet)
      </span>
      <a class="link ml-2" href="https://github.com/styts/tz-guestbook">
        <v-icon large>mdi-github</v-icon>
      </a>
    </v-app-bar>
    <v-main>
      <v-container>
        <nuxt />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  data () {
    return {
    }
  }
}
</script>

<style>
  .link {
    text-decoration: none;
  }
</style>
