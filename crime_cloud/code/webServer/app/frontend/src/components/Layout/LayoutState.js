export const initialState = {
  isSidebarOpened: false,
};

export const TOGGLE_SIDEBAR = "Layout/TOGGLE_SIDEBAR";

export const toggleSidebar = () => ({
  type: TOGGLE_SIDEBAR,
})

export default function LayoutReducer(state = initialState, { type, payload }) {
  // switch (type) {
  //   case TOGGLE_SIDEBAR:
      return {
        ...state,
        isSidebarOpened: !state.isSidebarOpened,
      };
  //   default:
  //     return state;
  // }
}
