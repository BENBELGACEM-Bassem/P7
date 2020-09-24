
function addWikiLink(elt){
	const wikiLink = document.createElement('a');
	wikiLink.innerText = "[En savoir plus sur Wikipedia]";
	wikiLink.href = elt.data['url'];
	wikiLink.style.color = "blue";
	wikiLink.style.textDecoration = "underline";
	return wikiLink;
}

function addGifLoader(){
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
	const loader = document.querySelector('#loader');
	loader.remove();
}

function addMap(elt){
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

	let statement ;
	if (infos !== ''){
		statement = elt.data[infos];
	}
	else {
		statement = elt.data;
	}

	const newText = document.createTextNode(catchphrase+statement);
	const newTag = document.createElement('h5');
	const newDiv = document.createElement('div');

	newDiv.classList.add('col-12');

	newTag.appendChild(newText);
	newDiv.appendChild(newTag);

	if (infos === 'location_data'){
		const wikiLink = addWikiLink(elt);		
		newTag.appendChild(wikiLink);
	} 

	const parent = document.querySelector('#chat_zone');
	parent.appendChild(newDiv);	
}


async function askGrandpy(input) {
	addGifLoader()
	try{
		const resp = await axios.post('/ajax', new FormData(input));
		removeGifLoader();
		fillInChatBox(resp, 'adress', "Bien sûr mon poussin ! La voici : ");
		addMap(resp);
		fillInChatBox(resp, 'location_data', "Mais t'ai-je déjà raconté l'histoire de ce quartier qui m'a vu en culottes courtes ? ");
	}
	catch(e){
		removeGifLoader();
		e.data = "Hein, j'ai les oreilles rouillés !";
		fillInChatBox(e);	
	}
}

const form = document.querySelector("#question");
form.addEventListener("submit", function(event){
    event.preventDefault();
    addUserQuestion();
	askGrandpy(form);
});












