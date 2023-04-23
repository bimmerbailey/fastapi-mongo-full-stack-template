import { defineStore } from 'pinia'
import { Styles } from '@/styles/styles'
import { darkModeKey, styleKey } from '@/styles/config'
import type { StyleStore } from '@/interfaces/Styles'

export const useStyleStore = defineStore('style', {
  state: (): StyleStore => ({
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
      if (!Styles[payload]) {
        return
      }

      if (typeof localStorage !== 'undefined') {
        localStorage.setItem(styleKey, payload)
      }

      const style = Styles[payload]

      for (const key of Object.keys(style)) {
        const keyValue: string = `${key}Style`
        this[keyValue] = style[key]
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
