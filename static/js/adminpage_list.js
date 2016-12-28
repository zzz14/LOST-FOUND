/**
 * Created with PyCharm.
 * User: Epsirom
 * Date: 13-12-3
 * Time: 下午11:12
 */
/*
*
 * 2016-12-23
 */
var timeOffset = 0;

function getSmartStatus(act) {
    if (act.status == 0) {
        return '未发布';
    } else if (act.status == 1) {
        return '认领中..'
    } else {
        return '认领完毕';
    }
}

function wrapTwoDigit(num) {
    if (num < 10) {
        return '0' + num;
    } else {
        return num;
    }
}

function getChsDate(dt) {
    return wrapTwoDigit(dt.getDate()) + '日';
}

function getChsMonthDay(dt) {
    return wrapTwoDigit(dt.getMonth() + 1) + '月' + getChsDate(dt);
}

function getChsFullDate(dt) {
    return dt.getFullYear() + '年' + getChsMonthDay(dt);
}

function getChsDay(dt) {
    var dayMap = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
    return dayMap[dt.getDay()];
}

function getTimeStr(dt) {
    return wrapTwoDigit(dt.getHours()) + ':' + wrapTwoDigit(dt.getMinutes());
}

function isSameYear(d1, d2) {
    return d1.getFullYear() == d2.getFullYear();
}

function isSameMonth(d1, d2) {
    return isSameYear(d1, d2) && (d1.getMonth() == d2.getMonth());
}

function isSameDay(d1, d2) {
    return isSameYear(d1, d2) && isSameMonth(d1, d2) && (d1.getDate() == d2.getDate());
}

function getSmartTimeRange(start_time) {
    var result = getChsFullDate(start_time) + ' ' + getChsDay(start_time) + ' ' + getTimeStr(start_time);

    return result;
}

function expand_long_text(dom) {
    var newhtml, par = $(dom).parent(), refdata = par.text().trim();
    dom = $(dom);
    refdata = refdata.substring(0, refdata.length - 3);
    newhtml = dom.attr('ref-data') + ' <a style="cursor:pointer;" ref-data="' + refdata + '" ref-hint="' + dom.text() + '" onclick="expand_long_text(this);">' + dom.attr('ref-hint') + '</a>';
    par.html(newhtml);
}

/*删除*/
function deleteact(actid){
    var i, len, curact, admpages = locals.adminpages;

    for(i = 0, len = admpages.length; i < len; ++i){
        if(admpages[i].id == actid){

            curact = admpages[i];
            break;
        }
    }
    var content = '确认删除<span style="color:red">'+'</span>已发布信息？';
    $('#modalcontent').html(content);
    $('#act-'+actid).css("background-color","#FFE4C4");
    $('#deleteid').val(actid);
    $('#delModal').modal({
      keyboard: false,
      backdrop:false
    });
}

function delConfirm(){
    var delid = $('#deleteid').val();
    console.info("delid:%d", delid);
    api.post('/api/a/adminpage/delete', {id: parseInt(delid)}, function () {
        window.location.reload();
    }, dftFail, function () {
        $('#act-'+delid).css("background-color","#FFF");
    });
}

function delCancel(){
    var delid = $('#deleteid').val();
    $('#act-'+delid).css("background-color","#FFF");
}

function createtips(){
    var duringbook = [], beforeact = [], duringact = [];
    $.each(locals.activities, function (i, act) {
        if (act.currentTime >= act.bookStart && act.currentTime <= act.bookEnd) {
            duringbook.push(act.id);
        } else if (act.currentTime >= act.bookEnd && act.currentTime <= act.startTime) {
            beforeact.push(act.id);
        } else if (act.currentTime >= act.startTime && act.currentTime <= act.endTime) {
            duringact.push(act.id);
        }
    });
    var id;
    for(id in duringbook){
        $('#del-'+duringbook[id]).popover({
            html: true,
            placement: 'top',
            title:'',
            content: '<span style="color:red;">活动正在订票中，不能删除!</span>',
            trigger: 'hover',
            container: 'body'
        });
    }
    for(id in beforeact){
        $('#del-'+beforeact[id]).popover({
            html: true,
            placement: 'top',
            title:'',
            content: '<span style="color:red;">活动已出票，不能删除!</span>',
            trigger: 'hover',
            container: 'body'
        });
    }
    for(id in duringact){
        $('#del-'+duringact[id]).popover({
            html: true,
            placement: 'top',
            title:'',
            content: '<span style="color:red;">活动正在进行中，不能删除!</span>',
            trigger: 'hover',
            container: 'body'
        });
    }
}
