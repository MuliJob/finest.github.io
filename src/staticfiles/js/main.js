document.addEventListener('DOMContentLoaded', function () {
    NProgress.start();
    NProgress.done();

    if (typeof $ !== 'undefined') {
      $(document).ajaxStart(function () {
          NProgress.start();
      });

      $(document).ajaxStop(function () {
          NProgress.done();
      });
  }
});
