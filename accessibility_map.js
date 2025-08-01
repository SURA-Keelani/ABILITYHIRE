o // JavaScript for Smart Accessibility Map Page with Google Maps API integration

let map;
let markers = [];
let directionsService;
let directionsRenderer;
let userLocation = null;
let currentLanguage = localStorage.getItem('abilityHireLang') || 'en';

async function populateCityDropdown() {
    const citySelect = document.getElementById('citySelect');
    citySelect.innerHTML = '';
    try {
        const res = await fetch('/api/cities');
        const data = await res.json();
        data.cities.forEach(city => {
            const option = document.createElement('option');
            option.value = city;
            option.textContent = city;
            citySelect.appendChild(option);
        });
        citySelect.value = 'Amman';
        geocodeCity('Amman');
    } catch (e) {
        // fallback to hardcoded
        ['Amman', 'Riyadh', 'Cairo', 'Dubai', 'Doha', 'Kuwait City', 'Manama', 'Muscat', 'Beirut', 'Jerusalem'].forEach(city => {
            const option = document.createElement('option');
            option.value = city;
            option.textContent = city;
            citySelect.appendChild(option);
        });
        citySelect.value = 'Amman';
        geocodeCity('Amman');
    }
}

async function initMap() {
    // Initialize the map centered on Jordan
    const jordanBounds = {
        north: 33.375,
        south: 29.185,
        east: 39.301,
        west: 34.956
    };
    const centerJordan = { lat: 31.9454, lng: 35.9284 }; // Approximate center of Jordan

    map = new google.maps.Map(document.getElementById('map'), {
        center: centerJordan,
        zoom: 8,
        mapTypeControl: false,
        restriction: {
            latLngBounds: jordanBounds,
            strictBounds: false,
        }
    });

    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer({ map: map, panel: document.getElementById('directionsPanel') });

    // Try to get user's current location and link with Google Maps GPS
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                userLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude,
                };
                map.setCenter(userLocation);
                addUserMarker(userLocation);

                // Reverse geocode to get city name and auto-select city
                const geocoder = new google.maps.Geocoder();
                const latlng = { lat: userLocation.lat, lng: userLocation.lng };
                geocoder.geocode({ location: latlng }, (results, status) => {
                    if (status === 'OK' && results[0]) {
                        let city = null;
                        for (const component of results[0].address_components) {
                            if (component.types.includes('locality')) {
                                city = component.long_name;
                                break;
                            }
                        }
                        if (city) {
                            const citySelect = document.getElementById('citySelect');
                            // Check if city is in the dropdown options
                            const options = Array.from(citySelect.options).map(opt => opt.value);
                            if (options.includes(city)) {
                                citySelect.value = city;
                                geocodeCity(city);
                            }
                        }
                    }
                });
            },
            () => {
                console.warn('Geolocation permission denied or unavailable.');
            }
        );
    } else {
        alert(currentLanguage === 'en' ? 'Geolocation is not supported by this browser.' : 'المتصفح لا يدعم تحديد الموقع الجغرافي.');
    }

    // Load accessible locations for Jordan
    loadAccessibleLocations(centerJordan);

    // Populate city select dropdown dynamically
    await populateCityDropdown();

    // Setup city filter change event
    const citySelect = document.getElementById('citySelect');
    citySelect.addEventListener('change', (e) => {
        const city = e.target.value;
        geocodeCity(city);
    });

    // Setup language toggle button
    document.getElementById('languageToggle').addEventListener('click', toggleLanguage);

    // Setup location submission form
    document.getElementById('locationForm').addEventListener('submit', submitNewLocation);
}

function addUserMarker(position) {
    new google.maps.Marker({
        position: position,
        map: map,
        title: currentLanguage === 'en' ? 'Your Location' : 'موقعك',
        icon: {
            path: google.maps.SymbolPath.CIRCLE,
            scale: 8,
            fillColor: '#4285F4',
            fillOpacity: 1,
            strokeWeight: 2,
            strokeColor: 'white',
        },
    });
}

function geocodeCity(cityName) {
    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({ address: cityName }, (results, status) => {
        if (status === 'OK' && results[0]) {
            const location = results[0].geometry.location;
            map.setCenter(location);
            map.setZoom(12);
            loadAccessibleLocations({ lat: location.lat(), lng: location.lng() });
        } else {
            alert(currentLanguage === 'en' ? 'City not found.' : 'المدينة غير موجودة.');
        }
    });
}

async function loadAccessibleLocations(center) {
    // Clear existing markers
    clearMarkers();

    // Use Google Maps Places API to search for accessible places in the current map bounds
    const service = new google.maps.places.PlacesService(map);

    // Define place types to search for
    const placeTypes = ['restaurant', 'hospital', 'school', 'university', 'parking', 'health', 'gym', 'library', 'point_of_interest'];

    // Define accessibility keywords to filter places (Google Places API does not have direct accessibility filter, so use keywords)
    const accessibilityKeywords = ['wheelchair accessible', 'accessible', 'disability friendly', 'handicap accessible'];

    // Get current map bounds
    const bounds = map.getBounds();

    if (!bounds) {
        console.warn('Map bounds not available yet.');
        return;
    }

    // Placeholder for AI-powered recommendations integration
    // Example: fetch recommendations from backend or Google Cloud Retail API
    // const aiRecommendations = await fetch('/api/ai_recommendations').then(res => res.json());

    // For each place type, perform a nearby search with accessibility keywords
    for (const type of placeTypes) {
        for (const keyword of accessibilityKeywords) {
            const request = {
                bounds: bounds,
                type: [type],
                keyword: keyword,
            };

            service.nearbySearch(request, (results, status) => {
                if (status === google.maps.places.PlacesServiceStatus.OK && results) {
                    results.forEach(place => {
                        if (!place.geometry || !place.geometry.location) return;

                        const marker = new google.maps.Marker({
                            map: map,
                            position: place.geometry.location,
                            title: place.name,
                            icon: getIconForType(type),
                        });

                        marker.addListener('click', () => {
                            showLocationInfo({
                                name: place.name,
                                position: {
                                    lat: place.geometry.location.lat(),
                                    lng: place.geometry.location.lng()
                                },
                                type: type,
                                features: [], // Features not available from Places API
                                address: place.vicinity || place.formatted_address || '',
                            }, marker);
                        });

                        markers.push(marker);
                    });
                }
            });
        }
    }
}

function getDemoLocations() {
    // Static demo data for accessible locations
    return [{
            name: currentLanguage === 'en' ? 'Accessible Hotel' : 'فندق مهيأ',
            position: { lat: 31.955, lng: 35.91 },
            type: 'hotel',
            features: ['elevator', 'wheelchair_ramp', 'accessible_toilet'],
            address: '123 Main St, Amman',
        },
        {
            name: currentLanguage === 'en' ? 'Accessible Restaurant' : 'مطعم مهيأ',
            position: { lat: 31.95, lng: 35.92 },
            type: 'restaurant',
            features: ['wheelchair_ramp', 'accessible_toilet', 'reserved_parking'],
            address: '456 Food Ave, Amman',
        },
        {
            name: currentLanguage === 'en' ? 'Rehabilitation Center' : 'مركز إعادة تأهيل',
            position: { lat: 31.96, lng: 35.89 },
            type: 'rehabilitation',
            features: ['wheelchair_seating', 'accessible_toilet'],
            address: '789 Rehab Rd, Amman',
        },
    ];
}

function getIconForType(type, features = []) {
    // Return icon URL or symbol based on location type and features
    const baseUrl = '/static/images/icons/';
    if (features.includes('elevator')) return baseUrl + 'elevator.png';
    if (features.includes('wheelchair_ramp')) return baseUrl + 'ramp.png';
    if (features.includes('accessible_toilet')) return baseUrl + 'toilet.png';
    if (features.includes('reserved_parking')) return baseUrl + 'parking.png';
    switch (type) {
        case 'hotel':
            return baseUrl + 'hotel_wheelchair.png';
        case 'restaurant':
            return baseUrl + 'restaurant_wheelchair.png';
        case 'school':
            return baseUrl + 'school_wheelchair.png';
        case 'university':
            return baseUrl + 'university_wheelchair.png';
        case 'parking':
            return baseUrl + 'parking_wheelchair.png';
        case 'rehabilitation':
            return baseUrl + 'rehabilitation_wheelchair.png';
        default:
            return baseUrl + 'default_wheelchair.png';
    }
}

function showLocationInfo(location, marker) {
    // Show features as icons
    let featuresHtml = '';
    location.features.forEach(f => {
        featuresHtml += `<img src="/static/images/icons/${f}.png" alt="${f}" title="${f}" style="width:24px;height:24px;margin-right:4px;">`;
    });

    const contentString = `
        <div>
            <h3>${location.name}</h3>
            <p><strong>${currentLanguage === 'en' ? 'Address' : 'العنوان'}:</strong> ${location.address}</p>
            <p><strong>${currentLanguage === 'en' ? 'Features' : 'الميزات'}:</strong> ${featuresHtml}</p>
            <button id="directionsBtn">${currentLanguage === 'en' ? 'Get Directions' : 'احصل على الاتجاهات'}</button>
        </div>
    `;

    const infoWindow = new google.maps.InfoWindow({ content: contentString });
    infoWindow.open(map, marker);

    google.maps.event.addListenerOnce(infoWindow, 'domready', () => {
        document.getElementById('directionsBtn').addEventListener('click', () => {
            if (userLocation) {
                calculateAndDisplayRoute(userLocation, location.position, infoWindow);
            } else {
                alert(currentLanguage === 'en' ? 'User location not available.' : 'موقع المستخدم غير متوفر.');
            }
        });
    });
}

function calculateAndDisplayRoute(origin, destination, infoWindow = null) {
    directionsService.route({
        origin: origin,
        destination: destination,
        travelMode: google.maps.TravelMode.DRIVING,
    }, (response, status) => {
        if (status === 'OK') {
            directionsRenderer.setDirections(response);
            const route = response.routes[0];
            const leg = route.legs[0];
            // Show distance and duration in info window
            if (infoWindow) {
                infoWindow.setContent(infoWindow.getContent() +
                    `<p><strong>${currentLanguage === 'en' ? 'Distance' : 'المسافة'}:</strong> ${leg.distance.text}</p>
                     <p><strong>${currentLanguage === 'en' ? 'Duration' : 'المدة'}:</strong> ${leg.duration.text}</p>`);
            } else {
                alert(
                    (currentLanguage === 'en' ? 'Distance: ' : 'المسافة: ') + leg.distance.text +
                    ', ' +
                    (currentLanguage === 'en' ? 'Duration: ' : 'المدة: ') + leg.duration.text
                );
            }
        } else {
            alert(currentLanguage === 'en' ? 'Directions request failed due to ' + status : 'فشل طلب الاتجاهات بسبب ' + status);
        }
    });
}

function calculateAndDisplayRoute(origin, destination) {
    directionsService.route({
            origin: origin,
            destination: destination,
            travelMode: google.maps.TravelMode.DRIVING,
        },
        (response, status) => {
            if (status === 'OK') {
                directionsRenderer.setDirections(response);
            } else {
                alert(currentLanguage === 'en' ? 'Directions request failed due to ' + status : 'فشل طلب الاتجاهات بسبب ' + status);
            }
        }
    );
}

function clearMarkers() {
    markers.forEach((marker) => marker.setMap(null));
    markers = [];
}

function toggleLanguage() {
    currentLanguage = currentLanguage === 'en' ? 'ar' : 'en';
    localStorage.setItem('abilityHireLang', currentLanguage);
    location.reload();
}

// Initialize map when window loads
window.initMap = initMap;

// New function to submit new location and add marker automatically
function submitNewLocation(event) {
    event.preventDefault();

    const name = document.getElementById('locationName').value.trim();
    const type = document.getElementById('locationType').value;
    const features = Array.from(document.querySelectorAll('input[name="features"]:checked')).map(el => el.value);
    const address = document.getElementById('locationAddress').value.trim();

    if (!name || !type || !address) {
        alert(currentLanguage === 'en' ? 'Please fill in all required fields.' : 'يرجى ملء جميع الحقول المطلوبة.');
        return;
    }

    // Geocode the address to get lat/lng
    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({ address: address }, (results, status) => {
        if (status === 'OK' && results[0]) {
            const location = results[0].geometry.location;

            // Add marker to map
            const marker = new google.maps.Marker({
                position: location,
                map: map,
                title: name,
                icon: getIconForType(type),
            });

            marker.addListener('click', () => {
                showLocationInfo({
                    name: name,
                    position: { lat: location.lat(), lng: location.lng() },
                    type: type,
                    features: features,
                    address: address,
                }, marker);
            });

            markers.push(marker);

            // Center map on new marker
            map.setCenter(location);
            map.setZoom(15);

            // Optionally, send the new location data to backend API here (not implemented)

            alert(currentLanguage === 'en' ? 'Location added successfully!' : 'تمت إضافة الموقع بنجاح!');

            // Reset form
            document.getElementById('locationForm').reset();
        } else {
            alert(currentLanguage === 'en' ? 'Address not found. Please enter a valid address.' : 'العنوان غير موجود. يرجى إدخال عنوان صالح.');
        }
    });
}