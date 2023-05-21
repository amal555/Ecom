

    //customer login with their email address and password

    $('.sign_div').on('click',function () {
        $('.login_in').addClass('d-none');
        $('.sign_up').removeClass('d-none');
    })
    $('.login_div').on('click',function () {
        $('.sign_up').addClass('d-none');
        $('.login_in').removeClass('d-none');
    })
    function customerLogin(){
        const username = $("input[name=username]").val();
        const password = $("input[name=pass]").val();
        $.ajax({
            url: "/ecom/user_login",
            type: "POST",
            timeout:60000, // set timeout to 1 minutes,
            headers: {
                "X-CSRFToken": $("input[name=csrfmiddlewaretoken]").val(),
            },
            data: JSON.stringify({
                password: password,
                username: username
            }),
            contentType: "application/json",
            success: function (data) {
                if (data.status === 200){
                    var url = "/ecom/homepage";
                    $(location).attr("href", url);
                }else{
                    alert(data.msg);
                }
            },
            error: function (jqXHR, exception) {
                console.log(exception);
            },
            });
    }
    function customerRegister() {
        const name = $("input[name=name]").val();
        const email = $("input[name=email]").val();
        const created_pass = $("input[name=pass_sign]").val();
        const username = $("input[name=username1]").val();
        $.ajax({
            url: "/ecom/create_user",
            type: "POST",
            timeout:60000, // set timeout to 1 minutes,
            headers: {
                "X-CSRFToken": $("input[name=csrfmiddlewaretoken]").val(),
            },
            data: JSON.stringify({
                name: name,
                email: email,
                username: username,
                password: created_pass
            }),
            contentType: "application/json",
            success: function (data) {
                alert(data.msg);
                $('.login_in').removeClass('d-none');
                $('.sign_up').addClass('d-none');
            },
            error: function (jqXHR, exception) {
                console.log(exception);
            },
            });
    }


