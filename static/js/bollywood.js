const input = document.getElementById("movieInput");
const datalist = document.getElementById("movieSuggestions");

// LOAD MOVIE LIST
fetch("/bollywood/movies")
  .then((res) => res.json())
  .then((data) => {
    datalist.innerHTML = "";
    data.forEach((movie) => {
      const option = document.createElement("option");
      option.value = movie;
      datalist.appendChild(option);
    });
  });

// SEARCH
window.search = function () {
  const type = document.getElementById("searchType").value;
  const value = input.value.trim();

  if (!value) return alert("Please enter a value");

  let url = "";

  if (type === "recommend") {
    url = `/bollywood/recommend?movie=${encodeURIComponent(value)}`;
  } else if (type === "genre") {
    url = `/bollywood/search/genre?genre=${encodeURIComponent(value)}`;
  } else if (type === "year") {
    url = `/bollywood/search/year?year=${encodeURIComponent(value)}`;
  } else if (type === "director") {
    url = `/bollywood/search/director?name=${encodeURIComponent(value)}`;
  } else if (type === "actors") {
    url = `/bollywood/search/actors?name=${encodeURIComponent(value)}`;
  }

  fetch(url)
    .then((res) => res.json())
    .then((data) => render(data));
};

function render(data) {
  const row = document.getElementById("results");
  row.innerHTML = "";

  if (!data.length) {
    row.innerHTML = "<p class='text-center'>No results found</p>";
    return;
  }

  data.forEach((m) => {
    row.innerHTML += `
      <div class="col-6 col-sm-4 col-md-3 col-lg-2">
        <div class="movie-card">
          <img src="${m.poster || "https://via.placeholder.com/300x450"}">
          <div class="movie-title">${m.title}</div>
           <div class="movie-title">
            ${m.title} ${m.year ? `(${m.year})` : ""}
          </div>
        </div>
      </div>`;
  });
}
