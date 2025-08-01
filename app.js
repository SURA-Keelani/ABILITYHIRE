// Google Maps Accessibility Map with bilingual support, filtering, sidebar, and directions

let map;
let directionsService;
let directionsRenderer;
let currentLang = 'en';

const locations = [{
        id: 1,
        name: { en: "Accessible Restaurant", ar: "مطعم مهيأ" },
        type: "food",
        coords: { lat: 24.7200, lng: 46.6800 },
        accessibility: {
            wheelchairRamp: true,
            brailleSigns: false,
            dedicatedEntrance: true,
            accessibleRestroom: true,
            assistanceAvailable: true
        }
    },
    {
        id: 2,
        name: { en: "Clinic with Accessibility", ar: "عيادة مهيأة" },
        type: "medical",
        coords: { lat: 24.7100, lng: 46.6700 },
        accessibility: {
            wheelchairRamp: true,
            brailleSigns: true,
            dedicatedEntrance: true,
            accessibleRestroom: true,
            assistanceAvailable: false
        }
    },
    {
        id: 3,
        name: { en: "Education Center", ar: "مركز تعليمي" },
        type: "education",
        coords: { lat: 24.7050, lng: 46.6600 },
        accessibility: {
            wheelchairRamp: true,
            brailleSigns: true,
            dedicatedEntrance: false,
            accessibleRestroom: true,
            assistanceAvailable: true
        }
    },
    {
        id: 4,
        name: { en: "Public Building", ar: "مبنى عام" },
        type: "services",
        coords: { lat: 24.7150, lng: 46.6900 },
        accessibility: {
            wheelchairRamp: false,
            brailleSigns: true,
            dedicatedEntrance: true,
            accessibleRestroom: false,
            assistanceAvailable: true
        }
    }
];

let markers = [];

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 24.7136, lng: 46.6753 },
        zoom: 12,
        mapTypeControl: false,
        streetViewControl: false,
        fullscreenControl: false,
        language: currentLang
    });

    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer({ map: map, suppressMarkers: true });

    createMarkers();
    updateSidebar();
    setupFilterListener();
    setupLangToggle();
}

function createMarkers() {
    clearMarkers();
    const selectedTypes = getSelectedTypes();

    locations.forEach(loc => {
        if (selectedTypes.length === 0 || selectedTypes.includes(loc.type)) {
            const marker = new google.maps.Marker({
                position: loc.coords,
                map: map,
                title: loc.name[currentLang]
            });

            const infoWindow = new google.maps.InfoWindow({
                content: createInfoWindowContent(loc)
            });

            marker.addListener("click", () => {
                infoWindow.open(map, marker);
            });

            markers.push({ marker, loc, infoWindow });
        }
    });
}

function clearMarkers() {
    markers.forEach(({ marker, infoWindow }) => {
        infoWindow.close();
        marker.setMap(null);
    });
    markers = [];
}

function createInfoWindowContent(loc) {
    const acc = loc.accessibility;
    return `
        <div>
            <strong>${loc.name[currentLang]}</strong><br/>
            <ul>
                <li>${currentLang === 'en' ? 'Wheelchair Ramp' : 'منحدر للكراسي المتحركة'}: ${acc.wheelchairRamp ? '✔️' : '❌'}</li>
                <li>${currentLang === 'en' ? 'Braille Signs' : 'علامات بريل'}: ${acc.brailleSigns ? '✔️' : '❌'}</li>
                <li>${currentLang === 'en' ? 'Dedicated Entrance' : 'مدخل مخصص'}: ${acc.dedicatedEntrance ? '✔️' : '❌'}</li>
                <li>${currentLang === 'en' ? 'Accessible Restroom' : 'مرحاض مهيأ'}: ${acc.accessibleRestroom ? '✔️' : '❌'}</li>
                <li>${currentLang === 'en' ? 'Assistance Available' : 'المساعدة متوفرة'}: ${acc.assistanceAvailable ? '✔️' : '❌'}</li>
            </ul>
            <button onclick="getDirections(${loc.coords.lat}, ${loc.coords.lng})">${currentLang === 'en' ? 'Get Directions' : 'الحصول على الاتجاهات'}</button>
        </div>
    `;
}

function getSelectedTypes() {
    const checkboxes = document.querySelectorAll('input[name="type"]:checked');
    return Array.from(checkboxes).map(cb => cb.value);
}

function setupFilterListener() {
    const filterForm = document.getElementById("filter-form");
    filterForm.addEventListener("change", () => {
        createMarkers();
        updateSidebar();
        clearDirections();
    });
}

function setupLangToggle() {
    const langToggle = document.getElementById("lang-toggle");
    langToggle.addEventListener("click", () => {
        currentLang = currentLang === "en" ? "ar" : "en";
        document.documentElement.lang = currentLang;
        document.documentElement.dir = currentLang === "ar" ? "rtl" : "ltr";
        updateUI();
    });
}

function updateUI() {
    // Update filter labels
    document.querySelector('label[for="type-food"]').textContent = currentLang === "en" ? "Food" : "طعام";
    document.querySelector('label[for="type-medical"]').textContent = currentLang === "en" ? "Medical" : "طبي";
    document.querySelector('label[for="type-education"]').textContent = currentLang === "en" ? "Education" : "تعليم";
    document.querySelector('label[for="type-services"]').textContent = currentLang === "en" ? "Services" : "خدمات";
    document.getElementById("lang-toggle").textContent = currentLang === "en" ? "العربية" : "English";

    createMarkers();
    updateSidebar();
    clearDirections();
}

function updateSidebar() {
    const sidebar = document.getElementById("sidebar");
    sidebar.innerHTML = "";

    const selectedTypes = getSelectedTypes();
    const filteredLocations = selectedTypes.length === 0 ? locations : locations.filter(loc => selectedTypes.includes(loc.type));

    if (filteredLocations.length === 0) {
        sidebar.innerHTML = currentLang === "en" ? "<p>No locations found.</p>" : "<p>لم يتم العثور على مواقع.</p>";
        return;
    }

    filteredLocations.forEach(loc => {
        const locDiv = document.createElement("div");
        locDiv.className = "location-item";
        locDiv.tabIndex = 0;
        locDiv.setAttribute("role", "button");
        locDiv.setAttribute("aria-pressed", "false");
        locDiv.setAttribute("aria-label", loc.name[currentLang]);
        locDiv.innerHTML = `
            <strong>${loc.name[currentLang]}</strong><br/>
            <ul>
                <li>${currentLang === "en" ? "Wheelchair Ramp" : "منحدر للكراسي المتحركة"}: ${loc.accessibility.wheelchairRamp ? "✔️" : "❌"}</li>
                <li>${currentLang === "en" ? "Braille Signs" : "علامات بريل"}: ${loc.accessibility.brailleSigns ? "✔️" : "❌"}</li>
                <li>${currentLang === "en" ? "Dedicated Entrance" : "مدخل مخصص"}: ${loc.accessibility.dedicatedEntrance ? "✔️" : "❌"}</li>
                <li>${currentLang === "en" ? "Accessible Restroom" : "مرحاض مهيأ"}: ${loc.accessibility.accessibleRestroom ? "✔️" : "❌"}</li>
                <li>${currentLang === "en" ? "Assistance Available" : "المساعدة متوفرة"}: ${loc.accessibility.assistanceAvailable ? "✔️" : "❌"}</li>
            </ul>
            <button class="directions-btn">${currentLang === "en" ? "Get Directions" : "الحصول على الاتجاهات"}</button>
        `;

        locDiv.querySelector(".directions-btn").addEventListener("click", () => {
            getDirections(loc.coords.lat, loc.coords.lng);
        });

        locDiv.addEventListener("click", () => {
            const markerObj = markers.find(m => m.loc.id === loc.id);
            if (markerObj) {
                markerObj.infoWindow.open(map, markerObj.marker);
                map.panTo(markerObj.marker.getPosition());
                map.setZoom(15);
            }
        });

        locDiv.addEventListener("keydown", (e) => {
            if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                locDiv.click();
            }
        });

        sidebar.appendChild(locDiv);
    });
}

function getDirections(lat, lng) {
    if (!navigator.geolocation) {
        alert(currentLang === "en" ? "Geolocation is not supported by your browser" : "الموقع الجغرافي غير مدعوم من متصفحك");
        return;
    }
    navigator.geolocation.getCurrentPosition(position => {
        const start = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
        const end = new google.maps.LatLng(lat, lng);
        directionsService.route({
                origin: start,
                destination: end,
                travelMode: google.maps.TravelMode.WALKING
            },
            (response, status) => {
                if (status === google.maps.DirectionsStatus.OK) {
                    directionsRenderer.setDirections(response);
                } else {
                    alert(currentLang === "en" ? "Directions request failed due to " + status : "فشل طلب الاتجاهات بسبب " + status);
                }
            }
        );
    }, () => {
        alert(currentLang === "en" ? "Unable to retrieve your location" : "غير قادر على تحديد موقعك");
    });
}

function clearDirections() {
    directionsRenderer.setDirections({ routes: [] });
}

window.initMap = initMap;