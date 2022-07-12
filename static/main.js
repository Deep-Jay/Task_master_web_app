function getTodayDate (){
    var today = new Date()
    document.getElementById("datein").value = today.getFullYear() + '-' + ('0' + (today.getMonth() + 1)).slice(-2) + '-' + ('0' + today.getDate()).slice(-2);
};

window.onload = function(){
    getTodayDate();
};