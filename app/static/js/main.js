'use strict'

const form = document.getElementById('consumerForm')


const denyEmptyInput = ()=>{
    const username = document.getElementById('username')
    if(username.value === ""){
        console.log('Falta informação')
    }
    console.log(username.value)    
}


const fillForm = (endereco) => {
    document.getElementById('address').value = endereco.logradouro
    document.getElementById('neighborhood').value = endereco.bairro
    document.getElementById('city').value = endereco.localidade
    document.getElementById('state').value = endereco.uf
}


const pesquisarCep = async() =>{
    try{
        let re = new RegExp("^\d{5}\-*\d{3}$")
        const zipcode = document.getElementById('zipcode').value
        if (re.test(zipcode)){
            console.log('cep valido!')
        }
        else{
            console.log('cep inválido!')
        }
        const url = `http://viacep.com.br/ws/${zipcode}/json/`
        const data = await fetch(url)
        const address = await data.json()
        // fetch(url).then(response => response.json()).then(console.log)
        // o codigo a cima usar se for trabalhar sem a função ser async
        fillForm(address)
    }

    catch(e){
        console.log(e)
    }
}

const cleanInputs = () =>{
    setTimeout(function(){
    document.getElementById('username').value = ""
    document.getElementById('email').value = ""
    document.getElementById('password').value = ""
    document.getElementById('address').value = ""
    document.getElementById('number').value = ""
    document.getElementById('zipcode').value = ""
    document.getElementById('neighborhood').value = ""
    document.getElementById('city').value = ""
    document.getElementById('state').value = ""
    },100)
}

// $(document).ready(function(){
//     $("#zipcode").mask("99999-999")
// })


document.getElementById('zipcode')
        .addEventListener('focusout', pesquisarCep)


document.getElementById('consumerForm')
        .addEventListener('submit', cleanInputs)





// document.getElementById('consumerForm')
//         .addEventListener('submit', denyEmptyInput)

