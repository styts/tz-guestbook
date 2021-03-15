<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="8" md="6" :loading="loading">
      <v-alert v-if="error" dismissible type="error">
        {{ error }}
      </v-alert>
      <v-alert v-if="confirming" type="info">
        Waiting to include the operation on the blockchain...
      </v-alert>
      <v-expansion-panels>
        <v-expansion-panel>
          <v-expansion-panel-header>
            Info
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <p>
              This is a trivial guestbook DApp on the Tezos blockchain.
            </p>
            <p>
              Tutorial: <a href="https://styts.com/your-first-tezos-dapp">Build your first DApp on Tezos in 2-4 hours</a>.
            </p>
            <p>
              The data is stored in a <a
                about="_blank"
                href="https://better-call.dev/edo2net/KT1NunBWtpABstxkqW7QJAfBWUbFHxn2zCXX/operations">smart
                contract</a> on the testnet. The testnet can be reset any time, so
              this data will likely get lost. The submitted messages are
              unfiltered, and might contain offensive content.
            </p>
          </v-expansion-panel-content>
        </v-expansion-panel>
        <v-expansion-panel>
          <v-expansion-panel-header>
            Post Message
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <div v-if="!sending">
              <v-text-field v-model="author" outlined label="Author" />
              <v-textarea v-model="message" class="mb-3" hide-details outlined label="Message" />
              <v-btn class="primary" @click="submit">
                Submit
              </v-btn>
            </div>
            <v-progress-circular
              v-else
              size="100"
              class="mt-2"
              color="primary"
              indeterminate />
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
      <v-progress-circular
        v-if="loading"
        size="100"
        class="mt-2"
        color="primary"
        indeterminate />
      <v-card v-for="(x, idx) in entries" :key="idx" class="mb-1">
        <v-card-text>
          Author: <strong>{{ x.author }}</strong> <br>
          Date: <strong>{{ x.date }}</strong>
          <!-- eslint-disable-next-line vue/no-v-html -->
          <div class="mt-3" v-html="x.entry" />
        </v-card-text>
      </v-card>
      </v-progress-circular>
    </v-col>
  </v-row>
</template>

<script>
import { TezosToolkit } from '@taquito/taquito'
import { BeaconWallet } from '@taquito/beacon-wallet'
import { formatRelative } from 'date-fns'

const contractAddress = 'KT1NunBWtpABstxkqW7QJAfBWUbFHxn2zCXX'

function escapeHtml (unsafe) {
  return unsafe
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;')
}

export default {
  components: {
  },
  data () {
    return {
      loading: true,
      sending: false,
      confirming: false,
      entries: [],
      author: '',
      message: '',
      error: null
    }
  },
  mounted () {
    this.Tezos = new TezosToolkit('https://edonet-tezos.giganode.io')
    this.refresh()
  },
  methods: {
    async refresh () {
      // Contract API
      this.loading = true
      this.error = null
      this.contract = await this.Tezos.contract.at(contractAddress)
      const storage = await this.contract.storage()

      // "zip" the three storage arrays together into objects
      const data = storage.authors.map(function (author, i) {
        return {
          author,
          entry: escapeHtml(storage.entries[i]).replace('\n', '<br>'),
          date: formatRelative(new Date(storage.dates[i]), new Date())
        }
      })
      this.entries = data
      this.loading = false
    },
    async submit () {
      this.error = null
      const walletOptions = {
        name: 'Tezos Guestbook'
      }
      const wallet = new BeaconWallet(walletOptions)

      try {
        await wallet.requestPermissions({
          network: {
            type: 'edonet'
          }
        })
      } catch (e) {
        this.error = e.description
        return
      }
      // const userAddress = await wallet.getPKH()
      // console.log(userAddress)

      this.Tezos.setProvider({ wallet })

      // wallet API
      const contract = await this.Tezos.wallet.at(contractAddress)

      this.sending = true
      let operation
      try {
        operation = await (contract.methods.default(
          // parameter order should match the entrypoint in the smart contract
          this.author,
          this.message
        ).send())
      } catch (e) {
        this.error = e.description
        this.sending = false
        return
      }
      this.sending = false

      this.confirming = true
      const opResult = await operation.confirmation()
      this.confirming = false
      if (opResult.completed) {
        this.refresh()
      } else {
        this.error = 'An error has occurred'
      }
    }
  }
}
</script>
