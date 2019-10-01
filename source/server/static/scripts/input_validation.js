function doInputValidation(event){
    event.preventDefault()
    regex= "^[a-zA-z](([a-zA-Z1-9]+)(?: ?))+"
    name = document.getElementById("person-name").value
    team = document.getElementById("person-team").value
    console.log(name.match(regex))
    if(name.match(regex) === null && team.match(regex) === null){
      console.log("no match")
      error_msg = document.getElementById("form_error_msg").style.display = "block"
    }
    else{
      document.getElementById("add-person-form").submit();
    }
  }