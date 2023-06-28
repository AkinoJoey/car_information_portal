// static/js/car.js

// document.addEventListener('DOMContentLoaded', function () {
//     const makerDropdown = document.getElementById('makerDropdown');
//     const modelDropdown = document.getElementById('modelDropdown');

//     makerDropdown.addEventListener('change', function () {
//         const makeId = makerDropdown.value;
//         if (makeId) {
//             fetchModels(makeId);
//         } else {
//             clearModels();
//         }
//     });

//     function fetchModels(makeId) {
//         const url = `models/?make_id=${makeId}`;
//         fetch(url)
//             .then(response => response.json())
//             .then(data => {
//                 clearModels();
//                 data.models.forEach(model => {
//                     const option = document.createElement('option');
//                     option.value = model.model_name;
//                     option.textContent = model.model_name;
//                     modelDropdown.appendChild(option);
//                 });
//             });
//     }

//     function clearModels() {
//         modelDropdown.innerHTML = '<option value="">Select Model</option>';
//     }
// });

document.addEventListener('DOMContentLoaded', function () {
    const makerDropdown = document.getElementById('id_maker');
    const modelDropdown = document.getElementById('id_model');

    makerDropdown.addEventListener('change', function () {
        const makeId = makerDropdown.value;
        if (makeId) {
            fetchModels(makeId);
        } else {
            clearModels();
        }
    });

    function fetchModels(makeId) {
        const url = `form/?maker=${makeId}`;
        fetch(url)
            .then(response => response.json())
            .then(data => {
                clearModels();
                data.models.forEach(model => {
                    const option = document.createElement('option');
                    option.value = model[0];
                    option.textContent = model[1];
                    modelDropdown.appendChild(option);
                });
            });
    }

    function clearModels() {
        modelDropdown.innerHTML = '<option value="">Select Model</option>';
    }
});