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
    var results = lunrIndex.search(query);
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
