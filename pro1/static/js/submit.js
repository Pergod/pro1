$(function () {
    var oExports = {
        initialize: fInitialize,
        encode: fEncode
    };
    oExports.initialize();

    function fInitialize() {
//        var that = this;

    }

    submitComment  = function (image_id) {
        var that = this;
        var oCmtIpt_id = "jsCmt" + image_id;
        var oCmtIpt = $('#'+oCmtIpt_id);

        var discuss_list_id = "discuss-list"+image_id;
        var oListDv = $('#'+discuss_list_id);

        var oCommentCnt_id = "comment_count"+image_id;
        var oCommentCnt = $('#'+oCommentCnt_id);

        var oMoreDic_id= "more-discuss"+image_id;
        var oMoreDic = $('#'+oMoreDic_id);
        // 点击添加评论
        var bSubmit = false;
        var sCmt = $.trim(oCmtIpt.val());
        // 评论为空不能提交
        if (!sCmt) {
            return alert('评论不能为空');
        }
        // 上一个提交没结束之前，不再提交新的评论
        if (bSubmit) {
            return;
        }
        bSubmit = true;
        $.ajax({
            url: '/addcomment/',
            type: 'post',
            dataType: 'json',
            data: {image_id: image_id, content: sCmt}
        }).done(function (oResult) {
            if (oResult.code !== 0) {
                return alert(oResult.msg || '提交失败，请重试');
            }
            // 清空输入框
            oCmtIpt.val('');
            // 渲染新的评论
            var sHtml = [
                '<li>',
                    '<a class="_4zhc5 _iqaka" title="', oResult.username, '" href="/profile/', oResult.user_id, '">',oResult.username, '</a> ',
                    '<span><span>', sCmt, '</span></span>',
                '</li>'].join('');
            oListDv.prepend(sHtml);
            //更新评论条数
            var comment_count_id = "comment_count"+image_id;
            var more_discuss_id = "more-discuss"+image_id;
            var cHtml = ['<li class="more_discuss" id=',more_discuss_id,'>',
                            '<a>',
                                '<span>全部 </span><span id=',comment_count_id,
                                '>',
                                oResult.comment_count,
                                '</span>',
                                '<span> 条评论</span></a>',
                        '</li>'].join('');
            oMoreDic.replaceWith('');
            oListDv.prepend(cHtml);
        }).fail(function (oResult) {
            alert(oResult.msg || '提交失败，请重试');
        }).always(function () {
            bSubmit = false;
        });
    }

    function fEncode(sStr, bDecode) {
        var aReplace =["&#39;", "'", "&quot;", '"', "&nbsp;", " ", "&gt;", ">", "&lt;", "<", "&amp;", "&", "&yen;", "¥"];
        !bDecode && aReplace.reverse();
        for (var i = 0, l = aReplace.length; i < l; i += 2) {
             sStr = sStr.replace(new RegExp(aReplace[i],'g'), aReplace[i+1]);
        }
        return sStr;
    };

});