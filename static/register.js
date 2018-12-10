function check() {
    var username = document.getElementById("username");
    if (username.value.length == 0){
        alert("用户名不能为空");
        username.focus();
        return false;
    }
    else if (username.value.length > username.maxLength){
        alert("用户名长度不能超过15");
        username.focus();
        return false;
    }
    var password = document.getElementById("password");
    var password_confirm = document.getElementById("password_confirm");
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
    var school = document.getElementById("school");
    if (school.value.length == 0){
        alert("学校不能为空");
        school.focus();
        return false;
    }
    var major= document.getElementById("major");
    if (major.value.length == 0){
        alert("专业不能为空");
        major.focus();
        return false;
    }
    var phone = document.getElementById("phone");
    if (phone.value.length != 11){
        alert("电话号码长度错误");
        phone.focus();
        return false;
    }
    return true;
}