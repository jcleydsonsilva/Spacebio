document.addEventListener('DOMContentLoaded', function () {
    var countdownElements = document.querySelectorAll('.countdown');
    countdownElements.forEach(function (element) {
        var launchDate = element.dataset.launchDate;
        updateCountdown(element, launchDate);
    });
});

function updateCountdown(element, launchDate) {
    var x = setInterval(function () {
        var now = new Date().getTime();
        var launchTime = new Date(launchDate).getTime();
        var distance = launchTime - now;

        if (distance < 0) {
            clearInterval(x);
            element.innerHTML = 'Launching!';
            // setTimeout(function () {
            //     // Código para mudar para o próximo lançamento mais breve
            // }, 10 * 60 * 1000); // 10 minutos em milissegundos
        } else {
            var days = Math.floor(distance / (1000 * 60 * 60 * 24));
            var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((distance % (1000 * 60)) / 1000);

            element.innerHTML = days + 'd ' + hours + 'h ' + minutes + 'm ' + seconds + 's ';
        }
    }, 1000);
}

// Atualiza o elemento HTML com o ID 'countdown' para exibir o tempo restante formatado
// var launchs = document.getElementsByClassName('countdown')
// Array.from(launchs).forEach(function (launch) {
//     launch.innerHTML = days + 'd ' + hours + 'h ' + minutes + 'm ' + seconds + 's ';
// });