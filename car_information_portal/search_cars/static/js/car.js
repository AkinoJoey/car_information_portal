// static/js/car.js

document.addEventListener("DOMContentLoaded", function () {
    const makerDropdown = document.getElementById("make");
    const modelDropdown = document.getElementById("model");

    makerDropdown.addEventListener("change", function () {
        const makeId = makerDropdown.value;
        console.log(makeId);
        fetchModels(makeId);
    })

    function fetchModels(makeId) {
        fetch('/get-car-models', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({makeId:makeId}),
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


