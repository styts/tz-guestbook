<template>
  <v-app dark>
    <v-app-bar clipped-left fixed app>
      <v-app-bar-title>
        Tezos Guestbook
      </v-app-bar-title>
      <v-spacer />
      <span class="net">
        Edonet (testnet)
      </span>
      <v-btn href="https://github.com/styts/tz-guestbook" large icon>
        <v-icon>mdi-github</v-icon>
      </v-btn>
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
