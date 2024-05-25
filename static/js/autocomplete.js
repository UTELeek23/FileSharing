let resultBox;
let inputBox;
document.addEventListener('DOMContentLoaded', function() {
    const fileNames = window.fileNames || []; // Đảm bảo fileNames là một mảng

    resultBox = document.querySelector('.result-box');
    inputBox = document.getElementById('input-box');
    console.log(fileNames);
    inputBox.onkeyup = function() {
        let result = [];
        let userData = inputBox.value;

        if (userData.length) {
            if (Array.isArray(fileNames)) {
                result = fileNames.filter((keyword) => {
                    return keyword.toLowerCase().includes(userData.toLowerCase());
                });
            } else {
                console.error('fileNames is not an array');
            }
        }
        console.log(result);
        display(result);
        if(!result.length){
            resultBox.innerHTML = '';
        }
    };
    function display(result){
        const content = result.map((list) => {
            return "<li onclick=selectInput(this)>" + list + "</li>";
        }).join('');
        resultBox.innerHTML = "<ul>" + content + "</ul>";
    }

});
    function selectInput(list){
    inputBox.value = list.innerHTML;
    resultBox.innerHTML = '';
    }

