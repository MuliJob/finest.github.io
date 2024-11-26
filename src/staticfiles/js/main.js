document.addEventListener('DOMContentLoaded', function () {
    NProgress.start();

    window.onload = function () {
        NProgress.done();
    };

    if (typeof $ !== 'undefined') {
      $(document).ajaxStart(function () {
          NProgress.start();
      });

      $(document).ajaxStop(function () {
          NProgress.done();
      });
  }
});
