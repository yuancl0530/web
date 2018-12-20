function register_check() {
    var username = document.getElementById("register_username");
    var reg = /^[a-zA-Z_]{1,20}$/
    console.log(reg.test(username.value))


    if (!reg.test(username.value)){
        alert("用户名不合法\n可包含字母，下划线，并且长度不超过20");
        username.focus();
        return false;
    }
    var password = document.getElementById("register_password");
    var password_confirm = document.getElementById("register_password_confirm");
    if (password.value.length == 0){
        alert("密码不能位为空");
        password.focus()
        return false;
    }
    else if (password.value != password_confirm.value) {
        alert("密码不一致");
        password.focus()
        return false;
    }
    var school = document.getElementById("register_school");
    if (school.value.length == 0){
        alert("学校不能为空");
        school.focus();
        return false;
    }
    var major= document.getElementById("register_major");
    if (major.value.length == 0){
        alert("专业不能为空");
        major.focus();
        return false;
    }
    var phone = document.getElementById("register_phone");
    if (phone.value.length != 11){
        alert("电话号码长度错误");
        phone.focus();
        return false;
    }
    return true;
}

function writeablog() {
    window.location.href='/blog/newblog'
}

function login_check() {
    var username = document.getElementById('login_username');
    var password = document.getElementById('login_password');

    if (username.value.length == 0){
        alert('用户名不能为空');
        username.focus();
        return false;
    }
    return true;
}


function dismiss(s) {
    var dom = document.getElementsByClassName(s)
    for (var i = 0;i < dom.length;++i){
        dom[i].style.display='none';
    }

}
