// store/index.ts
import { Store } from 'vuex';

export const state = () => ({
  token: '', // Initial token state
  searchTerm: '', // Initial search term state
});

export const mutations = {
  setToken(state: any, token: string) {
    state.token = token;
  },
  clearToken(state: any) {
    state.token = '';
  },
  setSearchTerm(state: any, newSearchTerm: string) {
    state.searchTerm = newSearchTerm;
  },
};

export const actions = {
    setToken({ commit }: Store<any>, token: string) {
      commit('setToken', token);
    },
    // Add your existing actions here
    setSearchTerm({ commit }: Store<any>, newSearchTerm: string) {
      commit('setSearchTerm', newSearchTerm);
    },
  };
  
export const getters = {
  // Add your existing getters here
  getSearchTerm(state: any) {
    return state.searchTerm;
  },
};