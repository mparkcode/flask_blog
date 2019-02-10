let num = 2

function add_field(type) {
    console.log('clicked')
    num += 1
    if(type=='file'){
        $("#study_form").append("<div id='input_group" + num + "'><p><input id='key" + num + "' type='text' required><input id='value" + num + "' type='" + type + "' name='photo" + num + "' required> <span onclick='delete_inputs(" + num + ")'>X<span></p><input type='hidden' id='field_to_be_submitted" + num + "'></div>");
    } else {
        $("#study_form").append("<div id='input_group" + num + "'><p><input id='key" + num + "' type='text' required><input id='value" + num + "' type='" + type + "' required> <span onclick='delete_inputs(" + num + ")'>X<span></p><input type='hidden' id='field_to_be_submitted" + num + "'></div>");
    }
}

function delete_inputs(num) {
    console.log('clicked')
    let inputGroupToDelete = document.getElementById('input_group' + num)
    console.log(inputGroupToDelete)
    inputGroupToDelete.parentNode.removeChild(inputGroupToDelete);
}


function changeName() {
    for (i = 0; i <= num; i++) {
        if (document.getElementById('input_group' + i)) {
            if(document.getElementById(`value${i}`).type=='file'){
                document.getElementById(`field_to_be_submitted${i}`).setAttribute("name", "photo" + i + " " + document.getElementById(`key${i}`).value)
            } else {
                document.getElementById(`field_to_be_submitted${i}`).setAttribute("name", document.getElementById(`key${i}`).value)
            }
            document.getElementById(`field_to_be_submitted${i}`).setAttribute("value", document.getElementById(`value${i}`).value)
            console.log('testing')
        } else {
            continue;
        }
    }
}

Date.prototype.toDateInputValue = (function () {
    var local = new Date(this);
    local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
    return local.toJSON().slice(0, 10);
});

window.onload = function () {
    document.getElementById('value0').value = new Date().toDateInputValue();
}