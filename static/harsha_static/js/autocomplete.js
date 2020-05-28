const search = document.getElementById('search-text');
const desti_text = document.getElementById('destination-text');
const start_date_html = document.getElementById('date-start');
const end_date_html=document.getElementById('date-end');
const num_travs_html=document.getElementById('flights-num-travs');
const num_child_html=document.getElementById('flights-num-child-travs');
//const mode_bool=document.getElementById('travel-mode');


const matchList = document.getElementById('match-list');
const trendList = document.getElementById('trend-list');

let states;

// Get states
const getStates = async () => {
 //console.log("inside the getStates function");
 const res = await fetch('https://gist.githubusercontent.com/tdreyno/4278655/raw/7b0762c09b519f40397e4c3e100b097d861f5588/airports.json');
 states = await res.json();
 //console.log(states);
};
// FIlter states
const searchStates = (searchText=searchText) => {
 // Get matches to current text input
 //console.log("inside search states function");
 let matches = states.filter(state => {
  const regex = new RegExp(`^${searchText}`, 'gi');
  return state.name.match(regex) || state.code.match(regex) || state.city.match(regex) || state.country.match(regex);
 });


 // Clear when input or matches are empty
 if (searchText.length === 0) {
  matches = [];
  matchList.innerHTML = '';  //matchList.innerHTML
 }
 outputHtml(matches.slice(0,5));
};

function handler(temp_city_var) {
  search.value=temp_city_var;
  matches = [];
  matchList.innerHTML = '';
  outputHtml(matches);

};

// Show results in HTML
function outputHtml(matches) {
 if (matches.length > 0) {
  const html = matches.map(
    match => `<div><div id="id_${match.name}" onclick ="handler('${match.code}')" style="cursor: pointer" class="card card-body mb-2">
    <h6>${match.name} (${match.code})
    <span class="text-primary">${match.country}</span></h6>
   </div></div>`
   )
   .join('');
  matchList.innerHTML = html;
 }
};


const searchStates2 = (searchText=searchText) => {
  // Get matches to current text input
  let matches2 = states.filter(state => {
   const regex2 = new RegExp(`^${searchText}`, 'gi');
   return state.name.match(regex2) || state.code.match(regex2) || state.city.match(regex2) || state.country.match(regex2);
  });
 
  // Clear when input or matches are empty
  if (searchText.length === 0) {
   matches2 = [];
   trendList.innerHTML = '';  //trendlist.innerHTML
  }
  outputHtml2(matches2.slice(0,5));
 };
 
 function handler2(temp_city_var) {
   if (search.value===temp_city_var){
   console.log("Source and Destination cannot be the same");
   desti_text.value='Source and Destination cannot be the same';
   }
   else{
   desti_text.value=temp_city_var;
   matches2 = [];
   trendList.innerHTML = '';
   outputHtml2(matches);
   }
 }
 
 // Show results in HTML
 function outputHtml2(matches2) {
  if (matches2.length > 0) {
   const html = matches2.map(
     match => `<div id="id_${match.name}" onclick ="handler2('${match.code}')" style="cursor: pointer" class="card card-body mb-2">
     <h6>${match.name} (${match.code}) 
     <span class="text-primary">${match.country} </h6>
    </div>`
    )
    //above is for trending modify it aswell to have both..
    .join('');
    trendList.innerHTML = html;
  }
 };

 function date_selector(var_date,var_req_typ) {
    console.log("in date selector function");
    window.alert(var_date);
    let d= new Date();
    if (var_req_typ==='Start'){
        if (var_date<d.getDate()){
            console.log("Cannot be less than today");
            window.alert("Cannot be less than today");
        }
        }
    else{
    if (var_req_typ==='End'){
        if (var_date<start_date_html.value){
            console.log("Cannot be less than start date");
            window.alert("Cannot be less than start date");
        }
    }
 }
 };

 function enable_disable_end_date_html() {
 let mode_bool = document.getElementById('travel-mode');
 console.log(mode_bool.checked);
 console.log('enable_disable_end_date_html');
   if (mode_bool.checked===false){
   end_date_html.disabled=false;
   end_date_html.setAttribute("style","cursor:pointer; ");
   console.log("enable_disable_end_date_html");
   console.log("disable");
   console.log("False");
   }
   else{
   end_date_html.disabled=true;
   end_date_html.setAttribute("style","cursor: not-allowed;");
   console.log("enable_disable_end_date_html");
   console.log("Enable");
    console.log("True");
   }
 };

//console.log("before window load");
window.addEventListener('DOMContentLoaded',getStates);
//console.log("after window load");
search.addEventListener('input', () => searchStates(searchText=search.value));
desti_text.addEventListener('input',  () => searchStates2(searchText=desti_text.value));
start_date_html.addEventListener('input', date_selector(start_date_html.value,"Start"));
end_date_html.addEventListener('input', date_selector(end_date_html.value,"End"));


function flights_submit_btn_on_click() {
   window.alert("inside button click function");
   console.log(search.value,desti_text.value,start_date_html.value,end_date_html.value);
   if (search.value===desti_text.value){
   window.alert("Source and Destination cannot be the same");
   }
   if (start_date_html.value>=end_date_html.value){
   window.alert("Start Date and End Date Cannot be the same");
   }
   window.alert("Somthing");
 }



//for the places extension

