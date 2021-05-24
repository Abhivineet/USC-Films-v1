var mov_img = document.getElementById("mov_img");
var tv_img = document.getElementById("tv_img");
var tv_text = document.getElementById("tv_banner");
var mov_text = document.getElementById("movie_banner");
var url = "https://vmdb571.azurewebsites.net"
var tv_paths = [];
var mov_paths = [];
var tv_names = [];
var mov_names = []
var home_url = url + "/get_home_data"

fetch(home_url).then(response => response.json()).then((data) => {
    for (var i = 0; i < data['movie'].length; i++) {
        mov_paths[i] = data["movie"][i]["backdrop_path"]
        mov_names[i] = data["movie"][i]["title"] + ' (' + data['movie'][i]["year"] + ')'
        tv_paths[i] = data["tv"][i]["backdrop_path"]
        tv_names[i] = data["tv"][i]["name"] + ' (' + data['tv'][i]["year"] + ')'
        
    }
}).catch((err) => {
    console.log(err);
}).then(()=> {
    var curIndex = 0;
var imgDuration = 5000;
function slideShow() {
    document.getElementById("mov_img").className += " fade-in";
    document.getElementById("tv_img").className += " fade-in";
    document.getElementById("tv_banner").className += " fade-in";
    document.getElementById("movie_banner").className += " fade-in";
    document.getElementById("mov_img").src = mov_paths[curIndex];
    document.getElementById("movie_banner").innerHTML = mov_names[curIndex];
    document.getElementById("tv_img").src = tv_paths[curIndex];
    document.getElementById("tv_banner").innerHTML = tv_names[curIndex];
    setTimeout(function () {
        document.getElementById("mov_img").className = "img_holders";
        document.getElementById("tv_img").className = "img_holders";
        document.getElementById("tv_banner").className = "banner";
        document.getElementById("movie_banner").className = "banner";
    }, 4000);
    curIndex++;
    if (curIndex == mov_paths.length) { curIndex = 0; }
    setTimeout(slideShow, imgDuration);
}
slideShow();
});

function openTab(evt, tab) {
    // Declare all variables
    var i, tabcontent, tablinks;

    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("nav_contents");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace("active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tab).style.display = "inline-block";
    evt.currentTarget.className += " active";
}


function resetThis() {
    document.getElementById("keyword").value = "";
    document.getElementById("category").selectedIndex = 0;
    document.getElementById("result_holder").innerHTML = "";
    document.getElementById("atbt13").style.display = "none";
    document.getElementById("atbt12").style.display = "None";
}

function getSearchResults() {
    var query = document.getElementById("keyword").value.replace(/ /g, "%20");
    var cat = document.getElementById("category").value
    var search_url = "https://vmdb571.azurewebsites.net/"
    if (query == "" || cat == "blank") {
        alert("Please enter valid values");
    }
    else {
        if (cat == "movies") {
            search_url += "search_movie"
        }
        else if (cat == "tv") {
            search_url += "search_tv"
        }
        else {
            search_url += "search_multi"
        }
    }
    search_url += "?query=" + query;
    var xhttp = new XMLHttpRequest();
    console.log(search_url);
    xhttp.open('GET', search_url, true);
    xhttp.send();
    xhttp.addEventListener('load', makeSearchBody);
}

function makeSearchBody() {
    const response = JSON.parse(this.response);
    if (response.length>0){
        const container = document.getElementById("result_holder");
    container.innerHTML = "";
    document.getElementById("search_footer_div").style.marginTop = "50px"
    document.getElementById("atbt12").style.display = "None"
    document.getElementById("atbt13").style.display = "block"
    // document.getElementById("atbt13").style.visibility = "visible";
    response.forEach((result, index) => {
        const content = `    <div class="result_card">
        <div class="result_holder">
            <div class="search_image_holder">
                <img src="${result['poster_path']}" onerror="posterImageError(this);">
            </div>
            <div class="result_text_holder">
                <div class="result_title">
                    ${result['title']}
                </div>
                <div class="result_info">
                    <div class="misc_data">${result['info']}</div>
                    <div class="votes"><span>&#9733; ${result['vote_average']}</span>&nbsp;&nbsp;${result['vote_count']} </div>
                    <div class="overview">${result['overview']}</div>
                    <button class="show_more" onclick="getMore('${result['type']}','${result['id']}')" }">Show more</button>
                </div>
            </div>
        </div>
    </div>`;
        container.innerHTML += content;
    })
    document.getElementById("result_holder").style.display = "block"
    document.getElementById("atbt13").style.display = "block"
    }
    else{
        document.getElementById("result_holder").style.display = "none";
        document.getElementById("atbt13").style.display = "none"
        document.getElementById("atbt12").style.display = "block"
        document.getElementById("search_footer_div").style.marginTop = "-25px"
    }
    

}
function getMore(type, id) {
    var getMoreUrl = "https://vmdb571.azurewebsites.net" + "/id_search" + "?type=" + type + "&id=" + id;
    console.log(getMoreUrl);
    var xhttp = new XMLHttpRequest();
    xhttp.open('GET', getMoreUrl, true);
    xhttp.send();
    xhttp.addEventListener('load', makeModalBody);
}

function makeModalBody() {
    const response = JSON.parse(this.response);
    document.getElementById("modal_image").src = response['backdrop'];
    document.getElementById("modal_title").innerHTML = response['name'] + " ";
    document.getElementById("modal_info").innerHTML = response['info'];
    document.getElementById("modal_info_symbol").innerHTML =   `<a target="_blank" rel="noopener noreferrer" href="https://www.themoviedb.org/${response['type']}/${response['id']}">&#9432;</a>`
    document.getElementById("modal_voter_rating").innerHTML = `&#9733;${response['rating']} <span style="color:black;">&nbsp;&nbsp ${response['votes']}</span>`
    document.getElementById("modal_overview").innerHTML = response['synopsis']
    document.getElementById("modal_lang").innerHTML = response['spoken_languages']

    var cast = response['cast'];
    var cast_rows = document.getElementsByClassName("cast_row")
    if (cast.length == 0) {
        for (i = 0; i < 2; i++) {
            cast_rows[i].style.display = "none";
        }
        document.getElementById("cast_head").style.display="none"
    }
    else{
        document.getElementById("cast_head").style.display="block"
        for (i = 0; i < 2; i++) {
            cast_rows[i].style.display = "block";
        }
        for (i=0; i<8; i++){
            if(i>(cast.length-1)){
                document.getElementById("cast"+(i+1)).style.display = "none"
            }
            else{
                document.getElementById("cast_img"+(i+1)).src = cast[i]['picture']
                document.getElementById("cast_name"+(i+1)).innerHTML = cast[i]['name']
                document.getElementById("cast_char"+(i+1)).innerHTML = cast[i]['character']
                document.getElementById("cast"+(i+1)).style.display = "inline-block"
            }
        }
    }
    var reviews = response['reviews']
    console.log(reviews);
    if (reviews.length == 0){
        document.getElementById("modal_review_holder").innerHTML
        for (i = 0; i < 5; i++){
            document.getElementById("review_"+(i+1)).style.display="none"
        }
    else{
        document.getElementById("modal_review_holder").style.display="block"
        for (i = 0; i < 5; i++){
            if(i>(reviews.length-1)){
                document.getElementById("review_"+(i+1)).style.display="none"
            }
            else{
                document.getElementById("review_title"+(i+1)).innerHTML = reviews[i]['author']
                document.getElementById("review_date"+(i+1)).innerHTML ="on " + reviews[i]['review_date']
                document.getElementById("review_rating"+(i+1)).innerHTML = "&#9733;" + reviews[i]['review_rating']
                document.getElementById("review_text"+(i+1)).innerHTML = reviews[i]['content']
                document.getElementById("review_"+(i+1)).style.display="block"
            }
        }
    }
    document.getElementById("modal_container").style.display = "block";
}

function closeModal(){
    document.getElementById("modal_image").src = ""
    document.getElementById("modal_title").innerHTML = ""
    document.getElementById("modal_info").innerHTML = ""
    document.getElementById("modal_voter_rating").innerHTML = ""
    document.getElementById("modal_overview").innerHTML = ""
    document.getElementById("modal_lang").innerHTML = ""

    document.getElementById("modal_container").style.display = "none";
}