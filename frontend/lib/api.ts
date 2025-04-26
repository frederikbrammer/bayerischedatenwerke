// API utility functions for communicating with our backend

const API_BASE_URL = 'http://localhost:8000/api';

export async function fetchCases(searchQuery = '') {
    try {
        const url = searchQuery
            ? `${API_BASE_URL}/cases/?search=${encodeURIComponent(searchQuery)}`
            : `${API_BASE_URL}/cases/`;

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error fetching cases:', error);
        return [];
    }
}

export async function fetchCaseById(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/cases/${id}`);

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error(`Error fetching case with id ${id}:`, error);
        return null;
    }
}

export async function fetchTrendStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats/`);

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error fetching trend stats:', error);
        return null;
    }
}

export async function fetchCarStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats/cars`);

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error fetching car stats:', error);
        return [];
    }
}

export async function fetchPartStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats/parts`);

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error fetching part stats:', error);
        return [];
    }
}

export async function fetchStatusStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats/status`);

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error fetching status stats:', error);
        return [];
    }
}
