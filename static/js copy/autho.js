// auth.js
if (typeof window !== 'undefined') {
  window.saveToken = function (t) {
    localStorage.setItem('token', t);
    // optional: decode token to show username
  };
  window.getToken = function () { return localStorage.getItem('token'); };
  window.clearAuth = function () {
    localStorage.removeItem('token');
    localStorage.removeItem('user'); // if storing
  };
}
