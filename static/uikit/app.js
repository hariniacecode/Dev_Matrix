document.addEventListener('DOMContentLoaded', function () {

  let alertCloses = document.querySelectorAll('.alert__close');

  alertCloses.forEach((button) => {

    button.addEventListener('click', () => {

      let alert = button.parentElement;

      alert.style.display = 'none';

    });

  });

});