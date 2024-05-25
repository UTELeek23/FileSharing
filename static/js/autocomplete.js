let resultBox;
let inputBox;
document.addEventListener('DOMContentLoaded', function() {
    const fileNames = window.fileNames || []; // Đảm bảo fileNames là một mảng
    const jsonFileNames = window.JsonFiles;
    resultBox = document.querySelector('.result-box');
    inputBox = document.getElementById('input-box');
    // jsonFileNames.forEach((element) => {
    //     console.log(element.ID);
    //     console.log(element.Name);
    // });
    inputBox.onkeyup = function() {
        let result = [];
        let userData = inputBox.value;

        if (userData.length) {
            if (Array.isArray(fileNames)) {
                result = jsonFileNames.filter((keyword) => {
                    return keyword.Name.toLowerCase().includes(userData.toLowerCase());
                });
            } else {
                console.error('fileNames is not an array');
            }
        }
        display(result);
        if(!result.length){
            resultBox.innerHTML = '';
        }
    };
    function display(result) {
    const content = result.map((list) => {
        return `<a href="http://localhost:8000/ViewFiles/${list.ID}" style="text-decoration: none; color: #333333"><li onclick="selectInput(this)">ID: ${list.ID} | ${list.Name}</li></a>`;
    }).join('');
    resultBox.innerHTML = `<ul>${content}</ul>`;
    }


});
    function selectInput(list){
    inputBox.value = list.innerHTML;
    resultBox.innerHTML = '';
    }

