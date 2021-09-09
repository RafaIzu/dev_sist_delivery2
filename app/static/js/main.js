'use strict'

const form = document.getElementById('consumerForm')
const username = document.getElementById('username')

// const denyEmptyInput = ()=>{
//     const usernameInput = searchInput.value.trim()

//     if(!usernameInput){
//         console.log('favor não deixar vazio!')
//         document.getElementById('username').focus()
//         return True
//     }
// }


const fillForm = (endereco) => {
    document.getElementById('address').value = endereco.logradouro
}


const pesquisarCep = async() =>{
    const zipcode = document.getElementById('zipcode').value
    const url = `http://viacep.com.br/ws/${zipcode}/json/`
    const data = await fetch(url)
    const address = await data.json()
    // fetch(url).then(response => response.json()).then(console.log)
    // o codigo a cima usar se for trabalhar sem a função ser async
    fillForm(address)
}

document.getElementById('zipcode')
        .addEventListener('focusout', pesquisarCep)

// document.getElementById('consumerForm')
//         .addEventListener('submit', denyEmptyInput)

