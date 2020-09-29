'use strict';

function generate_csv() {
    var rows = $('#rows-number').val()
    var data = {rows: rows}
    var csrf_token = $('[name="csrfmiddlewaretoken"]').val()
    data['csrfmiddlewaretoken'] = csrf_token
    $.ajax({
        url: "generate_csv/",
        dataType: 'json',
        type: "POST",
        data: data,
        success: (json) => {
            data['task_id'] = json['task_id']
            data['csv_file_id'] = json['csv_file_id']
            var list_of_rows = document.querySelectorAll('[scope="row"]')
            $('#rows-number').val('');
            data['created'] = json['created']
            data['new_row_number'] = list_of_rows.length + 1
            $('table').append(`
                <tr>
                <th scope="row">${list_of_rows.length + 1}</th>
                <td>${data['created'].slice(0, 10)}</td>
                <td><button class="btn btn-secondary new-status-${data['new_row_number']}">Processing</button></td>
                <td class="new_row-${data['new_row_number']}"></td>
                </tr>
                `)
        },
        error: () => {
            console.log('Error')
        },
        complete: function check_task_status() {
            var continuePolling = true;
            setTimeout(function () {
                $.ajax({
                    url: `/check_task_status/${data['task_id']}/`,
                    success: function (json) {
                        data['task_result'] = json['result']
                        var new_action = $(`.new_row-${data['new_row_number']}`)
                        var new_status = $(`.new-status-${data['new_row_number']}`)
                        new_status[0].outerHTML = '<button class="btn btn-success">Ready</button>'
                        new_action.append(
                            `<a href="download_csv/${data['csv_file_id']}/">
                                <button class="btn btn-primary">Download</button>
                             </a>`)
                        if (data['task_result'] === '"Ready"') {
                            continuePolling = false;
                        }
                    },
                    complete: function () {
                        if (continuePolling) {
                            check_task_status();
                        }
                    },
                })
            }, 1000);
        }
    });
}

$('#generate-csv-form').on('submit', function (event) {
    event.preventDefault();
    generate_csv();
});