const input = document.getElementById("movieInput");
const datalist = document.getElementById("movieSuggestions");

fetch("/hollywood/movies")
  .then((res) => res.json())
  .then((data) => {
    datalist.innerHTML = "";
    data.forEach((movie) => {
      const option = document.createElement("option");
      option.value = movie;
      datalist.appendChild(option);
    });
  });

function recommend() {
  const movie = input.value.trim();
  if (!movie) return alert("Please enter a movie name");

  fetch(`/hollywood/recommend?movie=${encodeURIComponent(movie)}`)
    .then((res) => res.json())
    .then((data) => render(data));
}

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
        </div>
      </div>`;
  });
}
