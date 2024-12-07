
hbnb = {
    // storage area for data obtained from API calls
    "data": {
        "places": [],
        "amenities": []
    },

    // messages to be displayed in website. e.g. errors, notifications, etc
    "msg": {
        "error": {
            "api": {
                "generic": "Unable to retrieve API data. Please ensure the server is active.",
            }
        }
    },

    showError: function(msg) {
        document.getElementById("error").innerHTML = msg
        document.getElementById("error").setAttribute('class', 'show');
    },
    hideLoader: function() {
        document.getElementById("loader").setAttribute('class', 'hide');
    },

filterPriceOptionsPopulate: function() {
    let options = [50, 100, 250, 500]
    let selectElem = document.querySelector("#filter li.price select")

    for (let option of options) {
        selectElem.innerHTML += `
            <option value="` + option + `">
                $` + option.toString() + `
            </option>
        `;
    }
}
init: function() {
    const pageId = document.getElementsByTagName('body')[0].getAttribute('page-id')

    hbnb.loggedInStateUpdate();
    hbnb.logoutInit();

    switch(pageId) {
        case 'index':
            // 1. Load data for Amenities + Places
            hbnb.loadIndexData()
            .then(() => {
                // 2. Populate filter with data
                hbnb.filterAmenityCheckboxesPopulate()
                hbnb.filterPriceOptionsPopulate()

                // 3. Add Places data to website DOM
                hbnb.placesPopulate()

                // 4. Prepare the filter
                hbnb.filterSearchInit()
            }).catch((e) => {
                console.error(e)
            }).finally(() => {
                // Hide the loader
                hbnb.hideLoader()
            })
            break;
        case 'login':
            // TODO:
            break;
        case 'place':
            // TODO:
            break;
        case 'add_review':
            // TODO:
            break;
    }

    hbnb.loginModalInit();
  }
}

window.onload = function() {
hbnb.init();
}