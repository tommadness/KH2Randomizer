// Global variables
var lunrIndex;  // Lunr index
var pagesIndex; // JSON-loaded pages
// Search result weave: https://liveweave.com/t6I3lh

/**
 * Calculates the color based on the score for visual representation.
 * @param {number} score - The score to determine the color.
 * @param {number} [maxScore=5] - The maximum score for a perfect match.
 * @returns {string} The color in RGB format.
 */
function getScoreColor(score, maxScore = 5) {
  // max score determines the score at which a match is considered "perfect" visually
  const normalized = Math.min(Math.max(score / maxScore, 0), 1);

  const worstColor = { r: 128, g: 128, b: 128 }; // Gray
  const bestColor = { r: 99, g: 198, b: 245 };    // Blue
  
  const r = Math.round(worstColor.r + (bestColor.r - worstColor.r) * normalized);
  const g = Math.round(worstColor.g + (bestColor.g - worstColor.g) * normalized);
  const b = Math.round(worstColor.b + (bestColor.b - worstColor.b) * normalized);
  
  return `rgb(${r}, ${g}, ${b})`;
}

/**
 * Formats the search result for display.
 * @param {string} url - The URL of the page.
 * @param {string} title - The title of the page.
 * @param {string} matchedContent - The content that matched the search.
 * @param {number} score - The score of the match.
 * @param {string} displayedContent - The content to display.
 * @returns {string} The formatted HTML for the search result.
 */
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


/**
 * Fetches the JSON index and builds the Lunr index.
 * @returns {Promise} A promise that resolves when the index is built.
 */
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

/**
 * Performs the search based on the query and fuzzy search settings.
 * @param {string} query - The search query.
 * @param {number} fuzzySearch - The fuzzy search setting.
 * @param {number} [matchedCharsBefore=50] - The number of characters to display before the match.
 * @param {number} [matchedCharsAfter=100] - The number of characters to display after the match.
 * @returns {Array} An array of search results.
 */
function performSearch(query, fuzzySearch, matchedCharsBefore = 50, matchedCharsAfter = 100) {
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
        const firstMatchedTerm = matches[0];
        const matchedStartIndex = matchedPage.content.indexOf(firstMatchedTerm);
        return { 
          ...matchedPage, 
          score: result.score, 
          matchedText: firstMatchedTerm,
          displayedMatchText: matchedPage.content.slice(matchedStartIndex - matchedCharsBefore, matchedStartIndex + matchedCharsAfter)
        };
      });
    }
  }
  return []; // Return an empty array if query length is not more than 2
}

/**
 * Populates the search results based on the query and type.
 * @param {string} query - The search query.
 * @param {string} [type="menu"] - The type of search to perform.
 */
function populateSearch(query, type = "menu") {

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
  fetchAndBuildIndex().then(() => {
    const results = performSearch(query, fuzzySearch);
    if (results.length === 0) {
        resultsContainer.innerHTML += `<li><a>No results found.</a></li>`;
    } else {
        results.forEach(result => {
            if (type === "menu") {
                resultsContainer.innerHTML += `<li><a href="${result.url}">${result.title}</a></li>`;
            } else {
                resultsContainer.innerHTML += formatSubmittedSearchResult(
                    result.url,
                    result.title,
                    result.matchedText,
                    result.score,
                    result.displayedMatchText
                );
            }
        });
    }
  });
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

// this code will overwrite the main-content display from "none" to "block" 
// with either content or search results depending on the setting we're in
// this helps with avoiding flashes when hitting back and forward
document.addEventListener('DOMContentLoaded', function () {
  const urlParams = new URLSearchParams(window.location.search);
  const searchQuery = urlParams.get('search');
  const mainContent = document.querySelector('.main-content');

  if (searchQuery) {
      // Replace default content with search results
      mainContent.innerHTML = '<div id="submitted-search-results"></div>';
      populateSearch(decodeURIComponent(searchQuery), "page");
  }

  // Show the content after processing
  mainContent.style.display = 'block';
});

window.addEventListener('popstate', function (event) {
  const state = event.state;
  const searchQuery = state ? state.query : null;
  const mainContent = document.querySelector('.main-content');

  if (searchQuery) {
      // Replace default content with search results
      mainContent.innerHTML = '<div id="submitted-search-results"></div>';
      populateSearch(decodeURIComponent(searchQuery), "page");
  } else {
      // Restore default content
      mainContent.innerHTML = `{{ content }}`;
  }
  mainContent.style.display = 'block';
});




