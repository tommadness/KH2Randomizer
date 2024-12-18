// Global variables
var lunrIndex;  // Lunr index
var pagesIndex; // JSON-loaded pages

// Fetch the JSON index
fetch('/search.json')
  .then(response => response.json())
  .then(data => {
    pagesIndex = data;
    // Build Lunr index
    lunrIndex = lunr(function() {
      this.field('title', { boost: 10 });
      this.field('content');
      this.ref('url');

      pagesIndex.forEach(page => {
        this.add(page);
      });
    });
  });

// Listen for input changes
document.querySelector('.search-input').addEventListener('input', function(e) {
  var query = e.target.value.trim();
  var resultsContainer = document.querySelector('#search-results');
  resultsContainer.innerHTML = ''; // Clear old results

  if (query.length > 2) {  // Only search if 3+ chars
    // allow up to 2 edits of fuzzy search
    var results = lunrIndex.search(query + "~2");
    // results is an array of matches {ref: <url>, score: <number>}
    // We need to map them back to our pagesIndex
    results.forEach(result => {
      var matchedPage = pagesIndex.find(page => page.url === result.ref);
      if (matchedPage) {
        var li = document.createElement('li');
        li.innerHTML = `<a href="${matchedPage.url}">${matchedPage.title}</a>`;
        resultsContainer.appendChild(li);
      }
    });

    if (results.length === 0) {
      var li = document.createElement('li');
      li.textContent = 'No results found';
      resultsContainer.appendChild(li);
    }
  }
});

document.querySelector('.search-input').addEventListener('keydown', function(e) {
  if (e.key == 'Enter') {
    e.preventDefault();
    const query = e.target.value.trim();
    if (query) {
      const queryResultsURL = `${window.location.origin}?search=${encodeURIComponent(query)}`
      window.location.href = queryResultsURL;
    }
  }
})

document.addEventListener('DOMContentLoaded', function () {
  // Function to get query parameters
  function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
  }

  // Get the search term from the URL
  const searchQuery = getQueryParam('search');

  if (searchQuery) {
    const resultsContainer = document.querySelector('#search-results');
    const results = lunrIndex.search(searchQuery); // Perform Lunr.js search

    resultsContainer.innerHTML = ''; // Clear old results

    // Display results
    results.forEach(result => {
      const matchedPage = pagesIndex.find(page => page.url === result.ref);
      if (matchedPage) {
        const resultDiv = document.createElement('div');
        resultDiv.classList.add('search-result');
        resultDiv.innerHTML = `
          <h2><a href="${matchedPage.url}">${matchedPage.title}</a></h2>
          <p>${matchedPage.content.substring(0, 150)}...</p>
        `;
        resultsContainer.appendChild(resultDiv);
      }
    });

    if (results.length === 0) {
      resultsContainer.innerHTML = '<p>No results found.</p>';
    }
  }
});

