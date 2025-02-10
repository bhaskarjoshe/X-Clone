// registration form
const createAccountButton = document.querySelector('.open-registration-form')
const closeRegistrationForm = document.querySelector('.close-registration-form')
const registrationModal = document.querySelector('.registration-form')
const loginRedirect = document.querySelector('.login-redirect a')

createAccountButton.addEventListener('click', ()=>{
    registrationModal.showModal()
})

closeRegistrationForm.addEventListener('click', ()=>{
    registrationModal.close()
})

loginRedirect.addEventListener('click', (event)=>{
    event.preventDefault()
    registrationModal.close()
    loginModal.showModal()
})

// Registering a user
const form = document.querySelector('.registration-input')
const submitButton = form.querySelector("button[type='submit']")

form.addEventListener('submit', async function(event){
    event.preventDefault()

    const username = document.getElementById("name").value
    const email = document.getElementById("email").value
    const password = document.getElementById("password").value
    const errorDiv = document.querySelector('.registration-error')

    const formData = {
        username: username,
        email: email,
        password: password
    }

    try{
        const response = await fetch(registerApiUrl,{
            method: "POST",
            headers:{
                "Content-type": "application/json",
                'X-CSRFToken': document.querySelector("[name=csrfmiddlewaretoken]").value
            },
            body: JSON.stringify(formData)
        })

        const data = await response.json()
        if (response.ok){
            localStorage.setItem('auth_token', data.token)
            window.location.href = homepageUrl
        }
        else{
            errorDiv.textContent = data.error || "Username/Email already exists."
            errorDiv.style.visibility = "visible"
        }
        }
    catch(error){
        console.error("Error: ", error)
        errorDiv.textContent = "An error occurred. Please try again later."
        errorDiv.style.visibility = "visible"
        }
})


//login form
const openLoginFormButton = document.querySelector('.open-login-form')
const closeLoginFormButton = document.querySelector('.close-login-form')
const loginModal = document.querySelector('.login-form')
const registerRedirect = document.querySelector('.register-redirect a')
const errorDiv = document.querySelector(".login-error")

openLoginFormButton.addEventListener('click', () => {
    loginModal.showModal()
})

closeLoginFormButton.addEventListener('click', () => {
    loginModal.close()
})

registerRedirect.addEventListener('click', (event)=>{
    event.preventDefault()
    loginModal.close()
    registrationModal.showModal()
})

//loggin in a user
const inputForm = document.querySelector('.login-input')
const inputSubmitButton = inputForm.querySelector("button[type='submit']")

inputForm.addEventListener('submit',async function(event){
    event.preventDefault()

    const username = document.getElementById("login-name").value
    const password = document.getElementById("login-password").value

    const inputFormData = {
        username: username,
        password: password
    }

    try {
        const response = await fetch(loginApiUrl, {
            method : 'POST',
            headers:{
                'Content-type': "application/json",
                'X-CSRFToken': document.querySelector("[name=csrfmiddlewaretoken]").value
            },
            body: JSON.stringify(inputFormData)
        })

        const data = await response.json()
        if (response.ok){
            localStorage.setItem('auth_token', data.token)
            window.location.href = homepageUrl
        }
        else{
            errorDiv.textContent = data.error || "Invalid credentials.. Please try again."
            errorDiv.style.visibility = "visible"
        }
    }
    catch(error){
        console.error("Error: ", error)
        errorDiv.textContent = "An error occurred. Please try again later."
        errorDiv.style.visibility = "visible"
    }
})