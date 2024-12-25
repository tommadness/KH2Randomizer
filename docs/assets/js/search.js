// Global variables
var lunrIndex;  // Lunr index
var pagesIndex; // JSON-loaded pages
// Search result weave: https://liveweave.com/t6I3lh

function getScoreColor(score, maxScore=5) {
  // max score determines the score at which a match is considered "perfect" visually
  const normalized = Math.min(Math.max(score / maxScore, 0), 1);

  const worstColor = { r: 128, g: 128, b: 128 }; // Gray
  const bestColor = { r: 99, g: 198, b: 245 };    // Blue
  
  const r = Math.round(worstColor.r + (bestColor.r - worstColor.r) * normalized);
  const g = Math.round(worstColor.g + (bestColor.g - worstColor.g) * normalized);
  const b = Math.round(worstColor.b + (bestColor.b - worstColor.b) * normalized);
  
  return `rgb(${r}, ${g}, ${b})`;
}

function formatSubmittedSearchResult(url, title, matchedContent, score, displayedContent) {
  
  let snippet;
  const indexOfMatchedContent = displayedContent.indexOf(matchedContent);
  snippet = displayedContent.slice(0, indexOfMatchedContent) +
            '<span class="highlight">' + matchedContent + '</span>' +
            displayedContent.slice(indexOfMatchedContent + matchedContent.length);

  // Construct the search result HTML
  const searchResult = '<div class="search-result">' +
    '<div class="arrow">' +
        '<li></li>' +
    '</div>' +
    '<div class="search-result-content">' +
        '<a href="' + url + '" class="result-title">' +
        title +
        '</a>' +
        '<div class="result-snippet">' +
        snippet + // Use snippet instead of directly modifying displayedContent
        '</div>' +
        '<div class="result-score">' +
        '<span style="color: white; text-decoration: underline; text-underline-offset: 2.5px;">Match Score</span>:' +
        `<span style="color: ${getScoreColor(score)};"> ` + score.toFixed(2) + '</span>' +
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
    if (lunrIndex === null) {
      fetchAndBuildIndex();
    }

    var results = lunrIndex.search(query + "~" + fuzzySearch);
    if (results.length > 0) {
      return results.map(result => {
        const matchedPage = pagesIndex.find(page => page.url === result.ref);
        // get the matched term names
        const matches = Object.keys(result.matchData.metadata);
        const firstMatchedTerm = matches[0]
        const matchedStartIndex = matchedPage.content.indexOf(firstMatchedTerm);
        return { ...matchedPage, 
          score: result.score, 
          matchedText: firstMatchedTerm,
          displayedMatchText: matchedPage.content.slice(matchedStartIndex - matchedCharsBefore, matchedStartIndex + matchedCharsAfter)};
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
        resultsContainer.innerHTML += formatSubmittedSearchResult(result.url, result.title, result.matchedText, result.score, result.displayedMatchText);
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
