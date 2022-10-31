function ajouterInput(){
	var choix= document.getElementById("choix").value;
	var choix1=choix.substr(0,4);
	if(choix1=="CDAT"){
		document.getElementById("input_field1").innerHTML ="<label for='exampleFormControlInput1' class='form-label'>Tier</label><input class='form-control' name='tier' list='datalistOptions' id='exampleDataList' placeholder='Ajojouter un tiers'><datalist id='datalistOptions'><option selected></option>{% for element in tier %}<option value='{{element.nom}}'>{{element.nom}}</option>{% endfor %}</datalist>"; 
		document.getElementById("input_field2").innerHTML ="<input class='form-control' type='hidden' name='choix' value='oui'>"; 
		document.getElementById("input_field3").innerHTML ="<input class='form-control' type='hidden' name='choix1' value='non'>"; 
		

	}
	if(choix1=="CEAT"){
		
		document.getElementById("input_field1").innerHTML ="<label for='exampleFormControlInput1' class='form-label'>Tier</label><input class='form-control' name='tier' list='datalistOptions' id='exampleDataList' placeholder='Ajouter un tiers'><datalist id='datalistOptions'><option selected></option>{% for element in tier %}<option value='{{element.nom}}'>{{element.nom}}</option>{% endfor %}</datalist>"; 
		document.getElementById("input_field2").innerHTML ="<input class='form-control' type='hidden' name='choix' value='oui'>"; 
		document.getElementById("input_field3").innerHTML ="<input class='form-control' type='hidden' name='choix1' value='non'>"; 
		

	}
	if(choix1=="CDST"){
		document.getElementById("input_field1").innerHTML =""
		document.getElementById("input_field2").innerHTML ="<input class='form-control' type='hidden' name='choix' value='non'>"; 
		document.getElementById("input_field3").innerHTML ="<input class='form-control' type='hidden' name='choix1' value='non'>"; 
		
	}
	if(choix=="CEST"){
		document.getElementById("input_field1").innerHTML =""
		document.getElementById("input_field2").innerHTML ="<input class='form-control' type='hidden' name='choix' value='non'>"; 
		document.getElementById("input_field3").innerHTML ="<input class='form-control' type='hidden' name='choix1' value='non'>"; 
		
	}
	if(choix=="0"){
		document.getElementById("input_field1").innerHTML ="";
		document.getElementById("input_field2").innerHTML ="<input class='form-control' type='hidden' name='choix' value='non'>"; 
		document.getElementById("input_field3").innerHTML ="<input class='form-control' type='hidden' name='choix1' value='non'>"; 
		
	}
}
function gestionTiers(){
	var choix= document.getElementById("choix5").value;
	var choix1=choix.substr(0,4);
	if(choix1=="CDAT"){
		document.getElementById("input_field0").innerHTML ="<label for='exampleFormControlInput1' class='form-label'>Tier</label><input class='form-control' name='tier' list='datalistOptions' id='exampleDataList' placeholder='choix'><datalist id='datalistOptions'><option selected></option>{% for element in tier %}<option value='{{element.nom}}'>{{element.nom}}</option>{% endfor %}</datalist>"; 
	
	}
	if(choix1=="CEAT"){
		document.getElementById("input_field0").innerHTML ="<label for='exampleFormControlInput1' class='form-label'>Tier</label><input class='form-control' name='tier' list='datalistOptions' id='exampleDataList' placeholder='choix'><datalist id='datalistOptions'><option selected></option>{% for element in tier %}<option value='{{element.nom}}'>{{element.nom}}</option>{% endfor %}</datalist>"; 

	}
	if(choix1=="CDST"){
		document.getElementById("input_field0").innerHTML ="";
		
	}
	if(choix=="CEST"){
		document.getElementById("input_field0").innerHTML ="";
		
	}
	if(choix=="0"){
		document.getElementById("input_field2").innerHTML ="";
		
	}
}

element.setAttribute("disabled", "disabled");