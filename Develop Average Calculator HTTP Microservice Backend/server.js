const express = require('express');
const axios = require('axios');

const app = express();
const port = 9876;

// Define window size and window array to store numbers
const WINDOW_SIZE = 10;
let windowArray = [];

// Function to calculate average of numbers in window array
const calculateAverage = () => {
    if (windowArray.length === 0) return 0;
    const sum = windowArray.reduce((acc, num) => acc + num, 0);
    return sum / windowArray.length;
}

// Middleware to fetch even numbers from test server
const fetchEvenNumbers = async () => {
    try {
        const response = await axios.get('http://20.244.56.144/test/even');
        return response.data.numbers;
    } catch (error) {
        console.error('Error fetching even numbers:', error);
        return [];
    }
}

// Middleware to fetch prime numbers from test server
const fetchPrimeNumbers = async () => {
    try {
        const response = await axios.get('http://20.244.56.144/test/primes');
        return response.data.numbers;
    } catch (error) {
        console.error('Error fetching prime numbers:', error);
        return [];
    }
}

// Middleware to fetch Fibonacci numbers from test server
const fetchFibonacciNumbers = async () => {
    try {
        const response = await axios.get('http://20.244.56.144/test/fibo');
        return response.data.numbers;
    } catch (error) {
        console.error('Error fetching Fibonacci numbers:', error);
        return [];
    }
}

// Middleware to fetch random numbers from test server
const fetchRandomNumbers = async () => {
    try {
        const response = await axios.get('http://20.244.56.144/test/rand');
        return response.data.numbers;
    } catch (error) {
        console.error('Error fetching random numbers:', error);
        return [];
    }
}

// Middleware to handle request to /numbers/:numberid endpoint
app.get('/numbers/:numberid', async (req, res) => {
    const qualifiers = req.params.numberid.split(',');

    // Fetch numbers for all qualifiers from test servers
    const numbersPromises = qualifiers.map(async qualifier => {
        switch (qualifier) {
            case 'e':
                return fetchEvenNumbers();
            case 'p':
                return fetchPrimeNumbers();
            case 'f':
                return fetchFibonacciNumbers();
            case 'r':
                return fetchRandomNumbers();
            default:
                return [];
        }
    });
    const numbersArrays = await Promise.all(numbersPromises);
    const numbers = numbersArrays.flat(); // Flatten array of arrays

    if (numbers.length === 0) {
        res.status(500).send('Error fetching numbers from test servers');
        return;
    }

    // Add unique numbers to window array, ignoring duplicates
    numbers.forEach(num => {
        if (!windowArray.includes(num)) {
            windowArray.push(num);
        }
    });

    // Remove oldest number if window size is exceeded
    if (windowArray.length > WINDOW_SIZE) {
        windowArray.shift();
    }

    // Calculate average of current window
    const avg = calculateAverage();

    // Prepare response
    const response = {
        numbers: numbers,
        windowPrevState: [...windowArray],
        windowCurrState: [...windowArray],
        avg: avg.toFixed(2)
    };

    // Send response
    res.json(response);
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
