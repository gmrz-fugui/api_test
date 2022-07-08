function login() {
    let name = document.getElementById('username').value;
    let pwd = document.getElementById('password').value;
    let url= "http://127.0.0.1:5000/login"
    let data = {
        name: name,
        pwd: pwd
    }
    if (name==="" || pwd === ""){
        alert("用户名或密码错误，请重新输入！")
        showPopup()
        location.reload()
        return false
    }
    console.log(typeof data)
    console.log(data)
    $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        url: url,
        data: JSON.stringify(data),
        async: true,
        dataType: "json",
        success: function (result) {
            console.log(result)
            console.log(result.code)
            if (result.code === 0) {
                console.log('OK')
            } else {
                confirm(result.desc+"?")
                // location.reload()
            }
        },
        error: function (XMLHttpRequest, textStatus) {
            console.log(XMLHttpRequest.status, XMLHttpRequest.readyState, textStatus)
            alert('挂了')
        }
    })
}