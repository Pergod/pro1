$(function () {
    var oExports = {
        initialize: fInitialize,
    };
    oExports.initialize();

    function replaceLogBtn(oBtn){
       var btn =[
            '<button class="btn-primary-full"',
                'onclick="form=document.getElementById(','\'userform\'',');',
                'form.action=',
                '\'/login/\'',
                ';">',
                '登录</button>'
       ].join('');
      oBtn.replaceWith(btn);
    }

      function replaceRegBtn(oBtn){
       var btn =[
            '<button class="btn-primary-full"',
                'onclick="form=document.getElementById(','\'userform\'',');',
                'form.action=',
                '\'/register/\'',
                ';">',
                '注册</button>'
       ].join('');
      oBtn.replaceWith(btn);
    }

    function fInitialize() {
        var that = this;
        var oUserForm = $('#login-hd-id');
        var oBtn = $('#btn-id');
        $('#RegisterBtn').on('click', function () {
            var sHtml = [
                         '<div class="form-item">',
                            '<input class="input-txt"  aria-label="用户名" aria-required="true" autocapitalize="off" autocorrect="off" maxlength="30" name="name" placeholder="用户名" value="" type="text" data-reactid=".0.1.0.1.0.1.0.5.0">',
                        '</div>',
                        '<div class="form-item">',
                            '<input class="input-txt" aria-describedby="" aria-label="密码" aria-required="true" autocapitalize="off" autocorrect="off" name="password" placeholder="密码" type="password" value="" data-reactid=".0.1.0.1.0.1.0.6.0">',
                        '</div>',
                         '<div class="form-item">',
                            '<input class="input-txt" aria-describedby="" aria-label="邮箱" aria-required="true" autocapitalize="off" autocorrect="off" name="email" placeholder="邮箱" type="text" value="" data-reactid=".0.1.0.1.0.1.0.6.0">',
                        '</div>'].join('');
            oUserForm.after(sHtml);
            sHtml = [
                    '<div class="radio-wrapper">',
                        '<input name="role" type="radio" value="0" checked>普通用户</input>',
                        '<input name="role" type="radio" value="1">管理员</input>',
                    '</div>'].join('');
            oBtn.before(sHtml);
            replaceRegBtn(oBtn);
        });

        $('#LoginBtn').on('click', function () {
            var sHtml = [
                        '<div class="form-item">',
                            '<input class="input-txt"  aria-label="用户名" aria-required="true" autocapitalize="off" autocorrect="off" maxlength="30" name="name" placeholder="用户名" value="" type="text" data-reactid=".0.1.0.1.0.1.0.5.0">',
                        '</div>',
                        '<div class="form-item">',
                            '<input class="input-txt" aria-describedby="" aria-label="密码" aria-required="true" autocapitalize="off" autocorrect="off" name="password" placeholder="密码" type="password" value="" data-reactid=".0.1.0.1.0.1.0.6.0">',
                        '</div>'].join('');
            oUserForm.after(sHtml);
            replaceLogBtn(oBtn);
        });
    }
});