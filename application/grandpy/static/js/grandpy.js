
function addWikiLink(elt){
	// Add a link related to data displayed and style it 
	const wikiLink = document.createElement('a');
	wikiLink.innerText = "[En savoir plus sur Wikipedia]";
	wikiLink.href = elt.data['url'];
	wikiLink.style.color = "blue";
	wikiLink.style.textDecoration = "underline";
	return wikiLink;
}

function addGifLoader(){
	// Add and position a loader gif before displaying response to the user
	const newDiv = document.createElement('div');	
	const newImg = document.createElement('img');
	newImg.src = '../static/img/ajax_loading_icon.gif';
    newDiv.setAttribute('id', 'loader');
    newImg.setAttribute('alt', 'loading...');
    newImg.style.margin = "1rem 25rem "; 
	newDiv.appendChild(newImg);	
	const parent = document.querySelector('#chat_zone');
	parent.appendChild(newDiv);
}

function removeGifLoader(){
	// Remove the loder gif
	const loader = document.querySelector('#loader');
	loader.remove();
}

function addMap(elt){
	// Add a map view from google map Api and style it
    const newDiv = document.createElement('div');
    newDiv.setAttribute('id', 'map');
    newDiv.style.height = '70%';
    newDiv.style.width = '70%';
	newDiv.classList.add('col-9');
    const coordinates = {lat: elt.data['lat'], lng: elt.data['lng']};
    const map = new google.maps.Map(newDiv, {
      zoom: 15,
      center: coordinates
    });
    const marker = new google.maps.Marker({
      position: coordinates,
      map: map,
    });
	const parent = document.querySelector('#chat_zone');
	parent.appendChild(newDiv);

}

function addUserQuestion(){
	// Add the user question to the chat zone and style it
	const newDiv = document.createElement('div');
	const newTag = document.createElement('h5');
	newDiv.appendChild(newTag);
	newDiv.style.color = 'blue';
	newDiv.style.textAlign = 'right';
	newDiv.classList.add('col-12');
	const query = document.querySelector('#user_input');
	newTag.innerText = query.value;
	const parent = document.querySelector('#chat_zone');
	parent.appendChild(newDiv);
}

function fillInChatBox(elt, infos='', catchphrase=''){
	// Add data to the chat zone 

	// Create a variable to treat separatly error response from response with data
	let statement ;
	if (infos !== ''){
		statement = elt.data[infos];
	}
	else {
		statement = elt.data;
	}

	// Create an element to contain data retrieved 
	const newText = document.createTextNode(catchphrase+statement);
	const newTag = document.createElement('h5');
	const newDiv = document.createElement('div');
	// Style the element so it occupies the whole grid row
	newDiv.classList.add('col-12');
	// Put the element into a div tag
	newTag.appendChild(newText);
	newDiv.appendChild(newTag);

	// in case description is retrieved, a wiki link is added at its end
	if (infos === 'location_data'){
		const wikiLink = addWikiLink(elt);		
		newTag.appendChild(wikiLink);
	} 
	// Add the element to the chat zone
	const parent = document.querySelector('#chat_zone');
	parent.appendChild(newDiv);	
}


async function askGrandpy(input) {
	// Make a request to a server about a given input

	// Display the loader 
	addGifLoader()
	// Make a post request using axios librairy
	try{
		const resp = await axios.post('/ajax', new FormData(input));
		removeGifLoader();
		fillInChatBox(resp, 'adress', "Bien sûr mon poussin ! La voici : ");
		addMap(resp);
		fillInChatBox(resp, 'location_data', "Mais t'ai-je déjà raconté l'histoire de ce quartier qui m'a vu en culottes courtes ? ");
	}
	// Catch any error and display a message in the chat zone
	catch(e){
		removeGifLoader();
		e.data = "Hein, j'ai les oreilles rouillés !";
		fillInChatBox(e);	
	}
}

// Retrieve the user query element
const form = document.querySelector("#question");
form.addEventListener("submit", function(event){
	// Prevent the default behaviour of updating the whole page
    event.preventDefault();
    // Add the user question to the chat zone
    addUserQuestion();
    // Make the request from the frontend to the backend and display the answer 
	askGrandpy(form);
});












