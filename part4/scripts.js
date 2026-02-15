document.addEventListener('DOMContentLoaded', () => {

    /* ============================= */
    /*      LOGIN PAGE LOGIC         */
    /* ============================= */
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', loginUser);
    }

    /* ============================= */
    /*      INDEX PAGE LOGIC         */
    /* ============================= */
    if (document.getElementById('places-list')) {
        checkAuthenticationIndex();
    }

    /* ============================= */
    /*    PLACE DETAILS PAGE LOGIC   */
    /* ============================= */
    if (document.getElementById('place-details')) {
        initializePlacePage();
    }
});


/* ================================================= */
/*                    LOGIN                          */
/* ================================================= */

async function loginUser(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            document.cookie = `token=${data.access_token}; path=/`;
            window.location.href = 'index.html';
        } else {
            alert('Login failed. Check credentials.');
        }

    } catch (error) {
        console.error('Login error:', error);
        alert('API connection error.');
    }
}


/* ================================================= */
/*              COOKIE HANDLING                      */
/* ================================================= */

function getCookie(name) {
    const cookies = document.cookie.split(';');

    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) {
            return value;
        }
    }
    return null;
}


/* ================================================= */
/*                 INDEX PAGE                        */
/* ================================================= */

function checkAuthenticationIndex() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        loginLink.style.display = 'block';
        fetchPlaces();
    } else {
        loginLink.style.display = 'none';
        fetchPlaces(token);
    }
}


async function fetchPlaces(token = null) {

    try {
        const headers = {};

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
            method: 'GET',
            headers: headers
        });

        if (!response.ok) {
            throw new Error('Failed to fetch places');
        }

        const places = await response.json();
        displayPlaces(places);
        setupPriceFilter();

    } catch (error) {
        console.error(error);
        alert('Could not load places.');
    }
}


function displayPlaces(places) {

    const placesList = document.getElementById('places-list');
    placesList.innerHTML = '';

    places.forEach(place => {

        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.setAttribute('data-price', place.price);

        placeCard.innerHTML = `
            <h2>${place.name}</h2>
            <p>${place.description || ''}</p>
            <p><strong>Price:</strong> $${place.price}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;

        placesList.appendChild(placeCard);
    });
}


function setupPriceFilter() {

    const filter = document.getElementById('price-filter');
    if (!filter) return;

    filter.addEventListener('change', (event) => {

        const selectedPrice = event.target.value;
        const placeCards = document.querySelectorAll('.place-card');

        placeCards.forEach(card => {

            const placePrice = parseFloat(card.getAttribute('data-price'));

            if (selectedPrice === 'All') {
                card.style.display = 'block';
            } else if (placePrice <= parseFloat(selectedPrice)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
}


/* ================================================= */
/*              PLACE DETAILS PAGE                   */
/* ================================================= */

function initializePlacePage() {
    const placeId = getPlaceIdFromURL();
    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        if (addReviewSection) addReviewSection.style.display = 'none';
        if (loginLink) loginLink.style.display = 'block';
        fetchPlaceDetails(null, placeId);
    } else {
        if (addReviewSection) addReviewSection.style.display = 'block';
        if (loginLink) loginLink.style.display = 'none';
        fetchPlaceDetails(token, placeId);
    }
}


function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}


async function fetchPlaceDetails(token, placeId) {

    if (!placeId) {
        alert('No place ID provided.');
        return;
    }

    try {
        const headers = {};

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: headers
        });

        if (!response.ok) {
            throw new Error('Failed to fetch place details');
        }

        const place = await response.json();
        displayPlaceDetails(place);

    } catch (error) {
        console.error(error);
        alert('Could not load place details.');
    }
}


function displayPlaceDetails(place) {

    const section = document.getElementById('place-details');
    section.innerHTML = '';

    const container = document.createElement('div');
    container.className = 'place-info';

    container.innerHTML = `
        <h1>${place.name}</h1>
        <p><strong>Description:</strong> ${place.description || ''}</p>
        <p><strong>Price:</strong> $${place.price}</p>
        <p><strong>Amenities:</strong> ${place.amenities ? place.amenities.join(', ') : 'None'}</p>
        <h2>Reviews</h2>
    `;

    section.appendChild(container);

    if (place.reviews && place.reviews.length > 0) {
        place.reviews.forEach(review => {

            const reviewCard = document.createElement('div');
            reviewCard.className = 'review-card';

            reviewCard.innerHTML = `
                <p>${review.comment}</p>
                <p><strong>User:</strong> ${review.user || 'Anonymous'}</p>
                <p><strong>Rating:</strong> ${review.rating}/5</p>
            `;

            section.appendChild(reviewCard);
        });
    } else {
        const noReviews = document.createElement('p');
        noReviews.textContent = 'No reviews yet.';
        section.appendChild(noReviews);
    }
}
/* ================================================= */
/*                 ADD REVIEW PAGE                   */
/* ================================================= */

document.addEventListener('DOMContentLoaded', () => {

    const reviewForm = document.getElementById('review-form');

    if (reviewForm) {
        const token = checkAuthenticationForReview();
        const placeId = getPlaceIdFromURL();

        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const reviewText = document.getElementById('review-text').value;
            const rating = document.getElementById('rating').value;

            await submitReview(token, placeId, reviewText, rating);
        });
    }
});


/* ============================= */
/*  AUTH CHECK FOR ADD REVIEW    */
/* ============================= */

function checkAuthenticationForReview() {
    const token = getCookie('token');

    if (!token) {
        window.location.href = 'index.html';
    }

    return token;
}


/* ============================= */
/*       SUBMIT REVIEW           */
/* ============================= */

async function submitReview(token, placeId, reviewText, rating) {

    if (!placeId) {
        alert('No place selected.');
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/reviews', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                place_id: placeId,
                comment: reviewText,
                rating: parseInt(rating)
            })
        });

        handleReviewResponse(response);

    } catch (error) {
        console.error(error);
        alert('Error submitting review.');
    }
}


/* ============================= */
/*     HANDLE API RESPONSE       */
/* ============================= */

function handleReviewResponse(response) {

    if (response.ok) {
        alert('Review submitted successfully!');
        document.getElementById('review-form').reset();
    } else {
        alert('Failed to submit review.');
    }
}

