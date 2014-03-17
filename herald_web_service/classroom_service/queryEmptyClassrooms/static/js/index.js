// 查询今天
function queryToday() {
    quickQuery('today');
}

// 查询明天
function queryTomorrow() {
    quickQuery('tomorrow');
}

// 快捷搜索
function quickQuery(day) {
    var start = $('#q-start').val();
    var end = $('#q-end').val();
    var campus = $('#q-campus').val();

    $.mobile.loading("show");
    $.get('/queryEmptyClassrooms/query/' 
        + campus + '/' + day + '/' + start + '/' + end + '/', 
        function(data) {
            $.mobile.pageContainer.pagecontainer("change", "#resultPage");

            data = $.parseJSON(data);
            var ul = $('#resultList');
            ul.html("");
            
            for (var i = 0; i < data.length; i++) {
                ul.append('<li><a href="#">' + data[i] + '</a></li>').listview('refresh');
            }
        }).fail(function() {
            hint();
        }).always(function() {
            $.mobile.loading('hide');
        });
}

// 高级查询
function advancedQuery() {
    var weekNum = $('#week-num').val();
    var weekDay = $('#week-day').val();
    var start = $('#a-start').val();
    var end = $('#a-end').val();
    var campus = $('#a-campus').val();

    $.mobile.loading("show");
    $.get('/queryEmptyClassrooms/query/' 
        + campus + '/' + weekNum + '/' + weekDay + '/' + start + '/' + end + '/', 
        function(data) {
            $.mobile.pageContainer.pagecontainer("change", "#resultPage");

            data = $.parseJSON(data);
            var ul = $('#resultList');
            ul.html("");
            
            for (var i = 0; i < data.length; i++) {
                ul.append('<li><a href="#">' + data[i] + '</a></li>').listview('refresh');
            }
        }).fail(function() {
            hint();
        }).always(function() {
            $.mobile.loading('hide');
        });
}

// 提示错误
function hint() {
    $('#hintInfo').text('查询失败了QAQ，网络和输入不正确都可能会导致这样噢~');
    $('#hintLnk').trigger('click');
}