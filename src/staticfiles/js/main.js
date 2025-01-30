document.addEventListener('DOMContentLoaded', function () {
    NProgress.start();

    window.addEventListener('load', function () {
        NProgress.done();
    });

    document.querySelectorAll('a').forEach((link) => {
        link.addEventListener('click', function () {
            NProgress.start();
        });
    });
});
