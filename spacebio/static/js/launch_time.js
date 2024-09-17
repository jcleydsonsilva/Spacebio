document.addEventListener('DOMContentLoaded', function () {
    var countdownElements = document.querySelectorAll('.countdown');
    countdownElements.forEach(function (element) {
        var launchDate = element.dataset.launchDate;
        var windowEnd = element.dataset.windowEnd;
        updateCountdown(element, launchDate, windowEnd);
    });
});

function updateCountdown(element, launchDate, windowEnd) {
    var launchTimeUTC = Date.parse(launchDate);
    var windowEndUTC = Date.parse(windowEnd);

    if (isNaN(launchTimeUTC) || isNaN(windowEndUTC)) {
        console.error("Data de lançamento inválida: ", launchDate);
        element.innerHTML = "Data inválida!";
        return;
    }

    var x = setInterval(function () {
        var now = new Date().getTime();  // Horário atual do usuário
        var distanceToStart = launchTimeUTC - now;  // Tempo até o início do lançamento
        var distanceToEnd = windowEndUTC - now;  // Tempo até o fim da janela de lançamento

        if (distanceToEnd < 0) {
            clearInterval(x);
            element.innerHTML = 'Launch Finished';  // Lançamento finalizado
        } else if (distanceToStart < 0 && distanceToEnd > 0) {
            element.innerHTML = 'Launching!';  // Lançamento em andamento
        } else {
            var days = Math.floor(distanceToStart / (1000 * 60 * 60 * 24));
            var hours = Math.floor((distanceToStart % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            var minutes = Math.floor((distanceToStart % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((distanceToStart % (1000 * 60)) / 1000);

            element.innerHTML = days + 'd ' + hours + 'h ' + minutes + 'm ' + seconds + 's ';
        }
    }, 1000);
}


// Atualiza o elemento HTML com o ID 'countdown' para exibir o tempo restante formatado
// var launchs = document.getElementsByClassName('countdown')
// Array.from(launchs).forEach(function (launch) {
//     launch.innerHTML = days + 'd ' + hours + 'h ' + minutes + 'm ' + seconds + 's ';
// });