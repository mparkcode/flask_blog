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

function addNote() {
    document.getElementById(`field_to_be_submitted`).setAttribute("name", document.getElementById(`key`).value);
    document.getElementById(`field_to_be_submitted`).setAttribute("value", document.getElementById(`value`).value);
}

function addPicture(){
    document.getElementById(`field_to_be_submitted`).setAttribute("name", "photo " + document.getElementById(`key`).value);
    document.getElementById(`field_to_be_submitted`).setAttribute("value", document.getElementById(`value`).value);
}

Date.prototype.toDateInputValue = (function () {
    var local = new Date(this);
    local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
    return local.toJSON().slice(0, 10);
});

window.onload = function () {
    document.getElementById('value0').value = new Date().toDateInputValue();
}

function deleteElement(key, postId){
    var xhr = new XMLHttpRequest();
    
    xhr.open('POST', '/delete/' + postId + "/" + key);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
        if (xhr.status === 200) {
            document.getElementById(key).style.display = 'none';
        }
        else if (xhr.status !== 200) {
            alert('Fail');
        }
    };
    xhr.send();
}

function checkForNote(postId){
    if(document.getElementById('key').value != "" || document.getElementById('key').value != ""){
        console.log(`adding a note to ${postId}`)
        key = document.getElementById('key').value
        value = document.getElementById('value').value
        console.log(`${key} - ${value}`)
        var xhr = new XMLHttpRequest();
        xhr.open('POST', `/add_note/${postId}/${key}/${value}`);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.onload = function(data) {
            if (xhr.status === 200) {
                document.getElementById('post_detail').innerHTML += xhr.response;
                document.getElementById('key').value = "";
                document.getElementById('value').value = "";
            }
            else if (xhr.status !== 200) {
                alert('Fail');
            }
        };
        xhr.send();
    } else {
        console.log("Need a key and value");
    }
}

function showNoteForm(){
    document.getElementById('note_form').style.display = 'block';
}

function editNote(key){
    text = document.getElementById(`${key}title`).innerHTML;
    document.getElementById(`${key}title`).outerHTML = `<input id='${key}title' type='text' value='${text}' required>`;
}

document.onclick = function(){
    let postId = document.getElementById('postId').value;
    let post = {};
    let fields = document.querySelectorAll("[id*='group']");
    for(let i = 1; i <= fields.length; i++){
        let noteTitle;
        let v;
        if(document.getElementById(`${i}title`).nodeName == "INPUT"){
            noteTitle = document.getElementById(`${i}title`).value;
        } else {
            noteTitle = document.getElementById(`${i}title`).textContent;
        }
        if(document.getElementById(`${i}content`).nodeName == "INPUT"){
            v = document.getElementById(`${i}content`).value;
        } else {
            v = document.getElementById(`${i}content`).textContent;
        }
        post[i] = {"note" : { [noteTitle] : v}}
    }
    var xhr = new XMLHttpRequest();
    xhr.open('POST', `/update_post/${postId}`);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function(data) {
        if (xhr.status === 200) {
            let data = JSON.stringify(post)
        }
        else if (xhr.status !== 200) {
            alert('Fail');
        }
    };
    xhr.send();
}