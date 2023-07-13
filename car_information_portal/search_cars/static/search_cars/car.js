// 非同期でモデルリストを取得する
document.addEventListener("DOMContentLoaded", function () {
    const makerDropdown = document.getElementById("make");
    const modelDropdown = document.getElementById("model");

    makerDropdown.addEventListener("change", function () {
        const makeId = makerDropdown.value;
        fetchModels(makeId);
    })

    function fetchModels(makeId) {
        fetch('/get-car-models', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ makeId: makeId }),
        })
            .then(response => response.json())
            .then(data => {
                clearModels();
                data.forEach(data => {
                    const option = document.createElement('option');
                    option.value = data.model_name;
                    option.textContent = data.model_name;
                    modelDropdown.appendChild(option);
                });
            })
    }

    function clearModels() {
        modelDropdown.innerHTML = '<option value="">-- Select Model --</option>';
    }
})

// submitボタンを押した後、ページ遷移せずにモデルのデータを表示する
// test
document.getElementById('carForm').addEventListener('submit', () => function (event) {
    event.preventDefault();

    let formData = new FormData(this);

    fetch(window.location.href, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken') // CSRFトークンをリクエストヘッダーに含める
        }
    })
        .then(response => response.text())
        .then(data => {
            console.log(data);
        })
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}