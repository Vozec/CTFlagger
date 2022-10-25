['dragleave', 'drop', 'dragenter', 'dragover'].forEach(function (evt) {
    document.addEventListener(evt, function (e) {
        e.preventDefault();
    }, false);
});


var drop_area = document.getElementById('drop_area');
var fileList = undefined;


// Drag & Drop
drop_area.addEventListener('drop', function (e) {
        e.preventDefault();
    fileList = e.dataTransfer.files;
    if (fileList.length == 0) {
        return false;
    }
    document.getElementById('message_upload').textContent = `File Loaded : ${htmlEncode(jsEscape(fileList[0].name))}`;
}, false);

// Click
drop_area.addEventListener('change', (event) => {
    fileList = event.target.files;
    if (fileList.length == 0) {
        return false;
    }
    document.getElementById('message_upload').textContent = `File Loaded : ${htmlEncode(jsEscape(fileList[0].name))}`;
});

// Submit
var btn = document.getElementById('submit_button');
btn.addEventListener('click', (event) => {
   send_files()
});


function send_files() {
    var xhr = new XMLHttpRequest();
    xhr.open('post', '/upload', true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            window.location.href = window.location.href + JSON.parse(this.responseText).hash;
        }   
    }; 

    let pass = document.getElementById('PASSWORD').value
    let fflag   = document.getElementById('FFLAG').value

    var fd = new FormData();

    fd.append('password',pass)
    fd.append('fflag',fflag)

    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');    
    for (let file of fileList) {
        fd.append('files', file);
    }
    xhr.send(fd);
}

// Sécu 
function htmlEncode(str){
    return String(str).replace(/[^\w. ]/gi, function(c){
        return '&#'+c.charCodeAt(0)+';';
    });
}
function jsEscape(str){
    return String(str).replace(/[^\w. ]/gi, function(c){
        return '\\u'+('0000'+c.charCodeAt(0).toString(16)).slice(-4);
    });
}
