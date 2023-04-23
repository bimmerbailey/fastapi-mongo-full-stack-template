export interface StyleConfig {
  [index: string]: string
  /* Styles */
  aside: string
  asideScrollbars: string
  asideBrand: string
  asideMenuItem: string
  asideMenuItemActive: string
  asideMenuDropdown: string
  navBarItemLabel: string
  navBarItemLabelHover: string
  navBarItemLabelActiveColor: string
  overlay: string
}

export interface StylesI {
  [index: string]: StyleConfig
  basic: StyleConfig
  white: StyleConfig
}

export interface StyleStore {
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
