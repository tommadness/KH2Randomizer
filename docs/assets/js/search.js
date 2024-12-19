// Global variables
var lunrIndex;  // Lunr index
var pagesIndex; // JSON-loaded pages

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

function performSearch(query, fuzzySearch) {
  if (query.length > 2) { 
    // allow up to 2 edits of fuzzy search
    console.log("HERE COMES THE ");
    console.log(lunrIndex);
    if (lunrIndex === null) {
      fetchAndBuildIndex();
    }
    var results = lunrIndex.search(query + "~" + fuzzySearch);
    if (results.length > 0) {
      return results.map(result => {
        return pagesIndex.find(page => page.url === result.ref);
      });
    }
  }
  return []; // Return an empty array if query length is not more than 2
}

function populateSearch(query, type="menu") {

  const resultsContainer = document.querySelector(
    type == "menu"? "#search-results" : "#submitted-search-results"  
  );
  // match perfectly for menu, match off 1 character for full results display
  var fuzzySearch = type === "menu" ? 0 : 1; 

  // Clear old results and perform the search
  resultsContainer.innerHTML = '';
  var results = performSearch(query, fuzzySearch);
  console.log('Menu results:', results);
    
  // handle no results 
  if (results.length === 0) {
    resultsContainer.innerHTML += `<li><a>No results found.</a></li>`;
  } else { // populate #search-results in a similar way
    results.forEach(result => {
      resultsContainer.innerHTML += `<li><a href="${result.url}">${result.title}</a></li>`;
    });
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


