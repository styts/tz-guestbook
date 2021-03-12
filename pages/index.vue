<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="8" md="6" :loading="loading">
      <h1>
        Tezos Guestbook
      </h1>
      <span class="net">
        EdoNet (TestNet)
      </span>
      <br>
      <v-progress-circular
        v-if="loading"
        size="50"
        color="primary"
        indeterminate />
      <v-card v-for="(x, idx) in entries" :key="idx" class="mb-1">
        <v-card-text>
          Author: <strong>{{ x.author }}</strong> <br>
          Date: <strong>{{ x.date }}</strong>
          <div class="mt-3">
            {{ x.entry }}
          </div>
        </v-card-text>
      </v-card>
      </v-progress-circular>
    </v-col>
  </v-row>
</template>

<script>
import { TezosToolkit } from '@taquito/taquito'
import { formatRelative } from 'date-fns'

export default {
  components: {
  },
  data () {
    return {
      loading: true,
      entries: []
    }
  },
  async mounted () {
    const tezos = new TezosToolkit('https://edonet-tezos.giganode.io')
    const contractAddress = 'KT1NunBWtpABstxkqW7QJAfBWUbFHxn2zCXX'

    const contract = await tezos.contract.at(contractAddress)
    const storage = await contract.storage()

    // "zip" the three storage arrays together into objects
    const data = storage.authors.map(function (author, i) {
      return {
        author,
        entry: storage.entries[i],
        date: formatRelative(new Date(storage.dates[i]), new Date())
      }
    })

    this.entries = data
    this.loading = false
  }
}
</script>
