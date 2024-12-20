// Global variables
var lunrIndex;  // Lunr index
var pagesIndex; // JSON-loaded pages
// Search result weave: https://liveweave.com/t6I3lh

function formatSubmittedSearchResult(url, title, matchedContent, score) {
  var searchResult = '<div class="search-result">' +
    '<div class="arrow">' +
        '<li></li>' +
    '</div>' +
    '<div class="search-result-content">' +
        '<a href="' + url + '" class="result-title">' +
        title +
        '</a>' +
        '<div class="result-snippet">' +
        matchedContent +
        '</div>' +
        '<div class="result-score" style="color: red;">' +
        'Score: ' + score + 
        '</div>' +
    '</div>' +
  '</div>';
  return searchResult;
}

// Fetch the JSON index
// USE OF A PROMISE??????
function fetchAndBuildIndex() {
  return fetch('/search.json')
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
}
fetchAndBuildIndex();

function performSearch(query, fuzzySearch, matchedCharsBefore=50, matchedCharsAfter=100) {
  if (query.length > 2) { 
    // allow up to 2 edits of fuzzy search
    if (lunrIndex === null) {
      fetchAndBuildIndex();
    }

    var results = lunrIndex.search(query + "~" + fuzzySearch);
    if (results.length > 0) {
      return results.map(result => {
        const matchedPage = pagesIndex.find(page => page.url === result.ref);
        const matchedStartIndex = matchedPage.content.indexOf(query);
        return { ...matchedPage, score: result.score, matchedText: matchedPage.content.slice(matchedStartIndex - matchedCharsBefore, matchedStartIndex + matchedCharsAfter)};
      });
    }
  }
  return []; // Return an empty array if query length is not more than 2
}

function populateSearch(query, type="menu") {

  const resultsContainer = document.querySelector(
    type == "menu" ? "#search-results" : "#submitted-search-results"
  );
  if (type == "page") {
    document.querySelector("#search-results").innerHTML = '';
  }
  // match perfectly for menu, match off 1 character for full results display
  var fuzzySearch = type === "menu" ? 0 : 1; 

  // Clear old results and perform the search
  resultsContainer.innerHTML = '';
  var results = performSearch(query, fuzzySearch);
  console.log('Menu results attributes:', results.map(result => Object.entries(result)));
    
  // handle no results 
  if (type == "menu") {
    if (results.length === 0) {
      resultsContainer.innerHTML += `<li><a>No results found.</a></li>`;
    } else { // populate #search-results in a similar way
      results.forEach(result => {
        resultsContainer.innerHTML += `<li><a href="${result.url}">${result.title}</a></li>`;
      });
    }
  }
  if (type == "page") {
  if (results.length === 0) {
      resultsContainer.innerHTML += `<li><a>No results found.</a></li>`;
    } else { // populate #search-results in a similar way
      results.forEach(result => {
        resultsContainer.innerHTML += formatSubmittedSearchResult(result.url, result.title, result.matchedText, result.score);
      });
    }
  }
}

// Listen for input changes
document.querySelector('.search-input').addEventListener('input', function(e) {
  const query = e.target.value.trim();
  if (query) {
    populateSearch(query, type="menu")
  }
});

document.querySelector('.search-input').addEventListener('keydown', function(e) {
  if (e.key == 'Enter') {
    e.preventDefault();
    const query = e.target.value.trim();
    if (query) {

      // clear main content and only show results
      const mainContent = document.querySelector('.main-content');
      mainContent.innerHTML = '<div id="submitted-search-results"></div>';

      populateSearch(query, type="page")
      const queryResultsURL = `${window.location.origin}?search=${encodeURIComponent(query)}`
      window.history.pushState({ query }, '', queryResultsURL);
    }
  }
})

document.addEventListener('DOMContentLoaded', function () {
  const urlParams = new URLSearchParams(window.location.search);
  const searchQuery = urlParams.get('search');
  if (searchQuery) {

    // clear main content and only show results
    const mainContent = document.querySelector('.main-content');
    mainContent.innerHTML = '<div id="submitted-search-results"></div>';

    populateSearch(decodeURIComponent(searchQuery), type = "page");
  }
});

// Handle the popstate event
window.addEventListener('popstate', function (event) {
  const state = event.state;
  // retrieve the search query
  const searchQuery = state ? state.query : null; 
  
  if (searchQuery) {
    // clear main content and populate results
    const mainContent = document.querySelector('.main-content');
    mainContent.innerHTML = '<div id="submitted-search-results"></div>';
    populateSearch(decodeURIComponent(searchQuery), type = "page");
  }
});
