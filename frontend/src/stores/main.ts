import { defineStore } from 'pinia'
import axios from 'axios'

interface MainStore {
  [index: string]: string | null | boolean | Array<string>
  userName: string | null
  userEmail: string | null
  userAvatar: string | null

  /* Field focus with ctrl+k (to register only once) */
  isFieldFocusRegistered: boolean

  /* Sample data (commonly used) */
  clients: Array<string>
  history: Array<string>
}

export const useMainStore = defineStore('main', {
  state: (): MainStore => ({
    /* User */
    userName: null,
    userEmail: null,
    userAvatar: null,

    /* Field focus with ctrl+k (to register only once) */
    isFieldFocusRegistered: false,

    /* Sample data (commonly used) */
    clients: [],
    history: [],
  }),
  actions: {
    setUser(payload: any) {
      if (payload.name) {
        this.userName = payload.name
      }
      if (payload.email) {
        this.userEmail = payload.email
      }
      if (payload.avatar) {
        this.userAvatar = payload.avatar
      }
    },

    fetch(sampleDataKey: string) {
      axios
        .get(`data-sources/${sampleDataKey}.json`)
        .then((r) => {
          if (r.data && r.data.data) {
            this[sampleDataKey] = r.data.data
          }
        })
        .catch((error) => {
          alert(error.message)
        })
    },
  },
})
