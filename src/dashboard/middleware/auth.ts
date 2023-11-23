import { Route } from 'vue-router';

export default function ({ route, redirect }: { route: Route, redirect: Function }) {
  // Check if a token is present in localStorage
  const token = localStorage.getItem('token');

  if ((!token) && route.name !== 'login') {
    // If no token is found and the route is not the login page, redirect to the login page
    return redirect('/login');
  }
}