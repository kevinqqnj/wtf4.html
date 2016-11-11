


Vue.filter('toSmartDateKevin', function (timestamp) {
    var floor = ''
	if (typeof(timestamp)==='string') {
	if (timestamp.indexOf("楼 ") >= 0) {
		var arr = timestamp.split("楼 ");
		timestamp = arr[1];	// in floors: "63652楼 Sat, 29 Jan 2011 14:31:00 GMT"
		floor = arr[0]+"楼 ";
	}	
	if (timestamp.indexOf("GMT") >= 0) {
		timestamp = parseInt(Date.parse(timestamp)/1000);	// in floors: "Sat, 29 Jan 2011 14:31:00 GMT"
	}
        else {
	timestamp = (parseInt((new Date(timestamp)).getTime())/1000+28800) ; // in Logs:last_access: "1477884451" UTC -> GMT+8
	}
    }
    else if (isNaN(timestamp)) {
        return '';
    }
    else {
    timestamp = parseInt(timestamp); // Python time.time() is like: 1477884451.383(s)
    }
//    console.log(timestamp)
    var
        today = new Date(),
        now = today.getTime()/1000,      // Javascript getTime() is like: 1477884519957(ms), no "."
        s = '1分钟前',
        t = now - timestamp;
    if (t > 31104000) {
        // 12 months ago:
        s = Math.floor(t / 31104000) + '年前';
    }
    else if (t >= 2592000) {
        // 30-90 days ago:
        s = Math.floor(t / 2592000) + '个月前';
    }
    else if (t >= 86400) {
        // 1-30 days ago:
        s = Math.floor(t / 86400) + '天前';
    }
    else if (t >= 3600) {
        // 1-23 hours ago:
        s = Math.floor(t / 3600) + '小时前';
    }
    else if (t >= 60) {
        s = Math.floor(t / 60) + '分钟前';
    }
    return floor+s;
});

Vue.filter('toSmartDateKevin2', function (timestamp) {
    var floor = ''
	if (typeof(timestamp)==='string') {
	if (timestamp.indexOf("楼 ") >= 0) {
		var arr = timestamp.split("楼 ");
		timestamp = arr[1];	// in floors: "63652楼 Sat, 29 Jan 2011 14:31:00 GMT"
		floor = arr[0]+"楼 ";
	}	
	if (timestamp.indexOf("GMT") >= 0) {
		timestamp = parseInt(Date.parse(timestamp)/1000);	// in floors: "Sat, 29 Jan 2011 14:31:00 GMT"
	}
        else {
	timestamp = (parseInt((new Date(timestamp)).getTime())/1000+28800) ; // in Logs:last_access: "1477884451" UTC -> GMT+8
	}
    }
    else if (isNaN(timestamp)) {
        return '';
    }
    else {
    timestamp = parseInt(timestamp); // Python time.time() is like: 1477884451.383(s)
    }
//    console.log(timestamp)
    var that = new Date(timestamp*1000);
    var
        y = that.getFullYear(),
        m = that.getMonth() + 1,
        d = that.getDate(),
        hh = that.getHours(),
        mm = that.getMinutes();
//    s = y + '年' + m + '月' + d + '日' + hh + ':' + (mm < 10 ? '0' : '') + mm;
    s = y + '-' + m + '-' + d + ' ' + hh + ':' + (mm < 10 ? '0' : '') + mm;
    // or: return new Date(parseInt(nS) * 1000).toLocaleString()
    return s;
});



new Vue({
    el: '#app',
    data: {},
    validators: {  // 自定义的验证规则
        name: {
            check: function(val){  // val就是绑定的input/textarea的内容
                if(val.length < 15){
                    return val.replace(/(^\s*)|(\s*$)/g,"")  // 判断是否输入空字符
                }
            }
        },
    },
})

window.onpopstate = function(event) {
    var state = event.state
    if (state===null) {
    return null;
    }
    var pg = state.pg_his
  console.log("location: " + document.location + ", state: " + JSON.stringify(state) +", length:"+window.history.length)

  vm.gotoPage(page=pg, back=true)
};
