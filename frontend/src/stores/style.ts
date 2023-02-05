import {defineStore} from 'pinia'
import {basic} from '@/styles/styles'
import {darkModeKey, styleKey} from '@/styles/config'

interface StyleConfig {
  [index: string]: boolean | string

  /* Styles */
  asideStyle: string
  asideScrollbarsStyle: string
  asideBrandStyle: string
  asideMenuItemStyle: string
  asideMenuItemActiveStyle: string
  asideMenuDropdownStyle: string
  navBarItemLabelStyle: string
  navBarItemLabelHoverStyle: string
  navBarItemLabelActiveColorStyle: string
  overlayStyle: string

  /* Dark mode */
  darkMode: boolean
}

export const useStyleStore = defineStore('style', {
  state: (): StyleConfig => ({
    /* Styles */
    asideStyle: '',
    asideScrollbarsStyle: '',
    asideBrandStyle: '',
    asideMenuItemStyle: '',
    asideMenuItemActiveStyle: '',
    asideMenuDropdownStyle: '',
    navBarItemLabelStyle: '',
    navBarItemLabelHoverStyle: '',
    navBarItemLabelActiveColorStyle: '',
    overlayStyle: '',

    /* Dark mode */
    darkMode: true,
  }),
  actions: {
    setStyle(payload: string) {
      if (!basic) {
        return
      }

      if (typeof localStorage !== 'undefined') {
        localStorage.setItem(styleKey, payload)
      }

      for (const key of Object.keys(basic)) {
        const keyValue: string = `${key}Style`
        this[keyValue] = basic[key]
      }
    },

    setDarkMode(payload: boolean | null = null) {
      this.darkMode = payload !== null ? payload : !this.darkMode

      if (typeof localStorage !== 'undefined') {
        localStorage.setItem(darkModeKey, this.darkMode ? '1' : '0')
      }

      if (typeof document !== 'undefined') {
        document.body.classList[this.darkMode ? 'add' : 'remove'](
          'dark-scrollbars'
        )

        document.documentElement.classList[this.darkMode ? 'add' : 'remove'](
          'dark-scrollbars-compat'
        )
      }
    },
  },
})
