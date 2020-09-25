'use strict';
$(document).ready(function () {
    var generateBtn = $('.generate-btn');

    generateBtn.on('click', function (e) {
        $.ajax({
            url: 'generate_csv/',
            success: (data) => {
                var rows = document.querySelectorAll('[scope="row"]')
                var form_data = document.querySelector('form').rows.value

                console.log(form_data)

                $('table').append(`
                            <tr>
                            <th scope="row">${rows.length + 1}</th>
                            <td>${data['created'].slice(0, 10)}</td>
                            <td><button class="btn btn-secondary">Processing</button></td>
                            <td><a href="#"><button class="btn btn-primary">Download</button></a></td>
                            </tr>
                            `)
            }
        })
    })
});