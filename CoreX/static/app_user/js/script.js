document.addEventListener("DOMContentLoaded", function(){
    fetchUserInfo()
    fetchNonFollowedUsers()
    fetchFollowerFollowingCount()
    fetchCurrentUserTweets()
    document.getElementById("show-more-link").addEventListener("click", loadMoreNonFollowedPeople)
    document.getElementById("load-more-btn").addEventListener("click", loadMoreTweets)

})

let currentPage = 1
let nonFollowedPeopleCurrentPage = 1

// toggle between profile
const homepageToggle = document.querySelector('.go-to-homepage')
const searchToggle = document.querySelector('.go-to-searchbar')
const profileToggle = document.querySelector('.go-to-profile')


homepageToggle.addEventListener('click', (event)=>{
    window.location.href = homepageUrl  
})

searchToggle.addEventListener('click', (event)=>{
    const searchbar = document.querySelector(".search-bar")
    searchbar.focus()
})

profileToggle.addEventListener('click', (event)=>{
    window.location.href = profileUrl 
})


//fetch user info 
async function fetchUserInfo(){
    try{
        const response = await fetch(profileApiUrl)
        if (!response.ok){
            throw new Error('Failed to fetch user info')
        }
        const data = await response.json()
        showProfileInfo(data)
    }
    catch(error){
        console.log('Error Fetching User Info:', error)
    }
}

//updating profile wrt user
function showProfileInfo(data){
    const coverImage = document.getElementById('cover-image')
    coverImage.src = 'https://wallpapersok.com/images/high/explore-the-world-beyond-with-this-cute-astronaut-and-his-space-adventure-1ciddrzj8h1cfee5-1ciddrzj8h1cfee5.webp'

    const profileImage = document.getElementById('profile-image')
    profileImage.src = data.profile_picture || 
    'https://abs.twimg.com/sticky/default_profile_images/default_profile_400x400.png'

    const usernameElement = document.getElementById('username')
    const username= data.username.split('-')
                    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                    .join(' ')
    usernameElement.textContent = username
    
    
    const navCenter = document.querySelector('.navbar-center-username')
    navCenter.textContent = username

    if (data.is_power_user){
        usernameElement.classList.add('power-user')
    }
    else{
        usernameElement.classList.remove('power-user')
        const powerUserImage = document.querySelector('.power_user_logo')
        powerUserImage.style.display = 'None'
    }

    document.getElementById('bio').textContent = data.bio || ''
    document.getElementById('email').textContent = data.email.split('@')[0]
}

//updating follower and following count
async function fetchFollowerFollowingCount(){
    const followingCount = await fetchFollowingList()
    const followersCount = await fetchFollowersList()

    const followingCountElement = document.querySelector('.following-count')
    followingCountElement.innerText = followingCount.length
    const followersCountElement = document.querySelector('.followers-count')
    followersCountElement.innerText = followersCount.length

    return
}


//fetching following 
async function fetchFollowingList(){
    try{
        const response = await fetch(followingApiUrl)
        
        if(!response.ok){
            throw new Error('Failed to fetch following list')
        }
        data = (await response).json()
        return data
    }
    catch(error){
        console.log('Error fetching following List: ', error)
    }
}


//fetch followers
async function fetchFollowersList(){
    try{
        const response = await fetch(followersApiUrl)
        
        if(!response.ok){
            throw new Error('Failed to fetch followers list')
        }
        data = (await response).json()
        return data
    }
    catch(error){
        console.log('Error fetching followers List: ', error)
    }
}

//fetching non-followed users
async function fetchNonFollowedUsers(page = 1){
    try{
        const urlWithPageNo = `${nonFollowedUsersApiUrl}?page=${page}`
        const response = await fetch(urlWithPageNo)
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`)
        }
        
        const data = await response.json()

        const nonFollowedUserContainer = document.querySelector('.who-to-follow-people')
        
        nonFollowedUserContainer.innerHTML = ''
        
        data.forEach(nonFollowedUser => {
            const whoToFollowElement = document.createElement('div')
            whoToFollowElement.classList.add("who-to-follow-card")
            whoToFollowElement.innerHTML = `
            <div class='card-left-side'>
                <img src="https://abs.twimg.com/sticky/default_profile_images/default_profile_400x400.png" alt="Profile Picture" class="profile-pic">
                <div class="user-info">
                    <strong class="username">${nonFollowedUser.username}</strong>
                    <span class="email">@${nonFollowedUser.email.split('@')[0]}</span>
                </div>
            </div>
            <button class="follow-button" data-user-id="${nonFollowedUser.id}">Follow</button>
            `
            nonFollowedUserContainer.appendChild(whoToFollowElement)
        })
        
    }
    catch(error){
        console.log(error)
    }
}


//for show more  non followed people
async function loadMoreNonFollowedPeople(){
    nonFollowedPeopleCurrentPage++
    await fetchNonFollowedUsers(nonFollowedPeopleCurrentPage)
}


// follow / unfollow toggle
document.addEventListener('click', async (event)=>{
    if(event.target.classList.contains('follow-button')){
        const currentButton = event.target
        const currentButtonValue = currentButton.innerText
        const userId = currentButton.getAttribute('data-user-id')
        const apiUrl = `/follows/api/follow/${userId}/`

        if(currentButtonValue === `Follow`){
            try{
                const response = await fetch(apiUrl,{
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.querySelector("[name=csrfmiddlewaretoken]").value
                    }
                })

                if(!response.ok){
                    throw new Error(`HTTP error! status: ${response.status}`)
                }
            }
            catch(error){
                console.log(error)
            }

            currentButton.innerText = `Unfollow`
            currentButton.style.color = 'black'
            currentButton.style.backgroundColor = 'white'
        }
        else{
            try{
                
                const response = await fetch(apiUrl,{
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': document.querySelector("[name=csrfmiddlewaretoken]").value
                    }
                })

                if(!response.ok){
                    throw new Error(`HTTP error! status: ${response.status}`)
                }
            }
            catch(error){
                console.log(error)
            }
            currentButton.innerText = `Follow`
            currentButton.style.color = 'white'
            currentButton.style.backgroundColor = '#1da1f2' 
        }
    }
})


//temporary logout button (later on to be converted to a dropdown which takes to profile and logout)
const logoutButton = document.querySelector('.user-profile-button')
logoutButton.addEventListener('click', async () => {
    const response = await fetch(logoutUrl, {
        method: "DELETE",
        headers: {
            'X-CSRFToken': document.querySelector("[name=csrfmiddlewaretoken]").value
        }
    })
    if (response.ok) {
        localStorage.removeItem('auth_token')
        window.location.reload()
    }
})



//fetching current user tweets

async function fetchCurrentUserTweets(page = 1) {
    try {
        const currentUser = await fetchCurrentUser()
        const currentUserId = currentUser.id
        const isPowerUser = currentUser.is_power_user

        const urlWithPageNo = `/tweets/api/tweet/user/${currentUserId}/?page=${page}`
        const response = await fetch(urlWithPageNo)
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`)
        }
        const data = await response.json()
        const tweetContainer = document.querySelector(".profile-tweet-container")
        if (page === 1) {
            tweetContainer.innerHTML = ""
        }

        data.results.forEach(tweet => {
            const tweetElement = document.createElement("div")
            tweetElement.classList.add("tweet-card")
            tweetElement.setAttribute('data-tweet-id', tweet.id)
            
            const hasLiked = tweet.likes.find(like => like.user.id===currentUserId) !== undefined
            const likeButtonClass = hasLiked ? "liked" : ""
            const heartIconClass =  hasLiked ? "fa-solid": "fa-regular" 

            let editButton = ''
            if(tweet.author.id === currentUserId && isPowerUser){
                editButton=`
                    <span class="tweet-edit-icon" data-tweet-id="${tweet.id}" ">
                        <i class="fa-solid fa-user-pen edit-tweet-icon"></i>
                    </span>
                `
            }

            tweetElement.innerHTML = `
                <div class="tweet-header">
                    <img src="https://abs.twimg.com/sticky/default_profile_images/default_profile_400x400.png" alt="Profile" class="profile-pic">
                    <div class="tweet-user-info">
                        <strong>${tweet.author.username}</strong> 
                        <span class="tweet-email">@${tweet.author.email.split('@')[0]}</span>
                        <span class="tweet-date">${new Date(tweet.created_at).toLocaleString()}</span>
                    </div>
                    ${editButton}
                </div>
                <div class="tweet-content">
                    ${tweet.tweet_content}
                    ${renderMedia(tweet.media)}
                </div>
                <div class="tweet-actions" data-tweet-id='${tweet.id}'>
                    <span class="tweet-action"><i class="fa-regular fa-comment tweet-comment-icon"></i> ${tweet.comments.length}</span>
                    <span class="tweet-action"><i class="fa-solid fa-retweet"></i>0</span>
                    <span class="tweet-action ${likeButtonClass}"><i class="${heartIconClass} fa-heart like-tweet-icon ${likeButtonClass}"></i> ${tweet.likes.length}</span>
                    <span class="tweet-action"><i class="fa-solid fa-arrow-up-from-bracket"></i> Share</span>
                </div>
            `

            tweetContainer.appendChild(tweetElement)
        })

        if (!data.next) {
            document.getElementById('load-more-btn').style.display = "none"
        }

    } catch (error) {
        console.error("Error fetching tweets: ", error)
    }
}


//for next page (pagination)
async function loadMoreTweets() {
    currentPage++
    await fetchCurrentUserTweets(currentPage)
    
}

//rendering media files with tweets
function renderMedia(mediaArray) {
    if (!mediaArray || mediaArray.length === 0) return ""

    let mediaHtml = ""
    mediaArray.forEach(media => {
        const fileUrl = media.file

        if (fileUrl.endsWith(".jpg") || fileUrl.endsWith(".png") || fileUrl.endsWith(".jpeg") || fileUrl.endsWith(".gif") || fileUrl.endsWith(".webp")) {
            mediaHtml += `<img src="${fileUrl}" class="tweet-media" alt="Tweet media">`
        } else if (fileUrl.endsWith(".mp4") || fileUrl.endsWith(".webm") || fileUrl.endsWith(".ogg")) {
            mediaHtml += `<video controls class="tweet-media"><source src="${fileUrl}" type="video/mp4"></video>`
        }
    })
    return `<div class="tweet-media-container">${mediaHtml}</div>`
}


// getting current user
async function fetchCurrentUser() {
    try{
        const response = await fetch ('/user/api/profile/')
        if(response.ok){
            const data = await response.json()
            return data
        }
        else{
            console.log('Response error')
        }
    }
    catch(error)
    {
        console.error(error)
        return null
    }
}



//like unlike tweet
document.addEventListener("click", async (event) => {
    if (event.target.classList.contains("like-tweet-icon")) {
        const likeIcon = event.target
        const likeButton = likeIcon.closest(".tweet-action")
        const tweetAction = likeIcon.closest(".tweet-actions")
        const tweetId = tweetAction.getAttribute("data-tweet-id")

        const isLiked = likeButton.classList.contains("liked")
        const apiUrl = `/tweets/api/tweet/${tweetId}/${isLiked ? "unlike" : "like"}/`
        const method = isLiked ? "DELETE" : "POST"

        try {
            const response = await fetch(apiUrl, {
                method: method,
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
                }
            })

            if (response.ok) {
                toggleLikeUI(likeButton, likeIcon, isLiked)
            } else {
                console.error(`Error ${isLiked ? "unliking" : "liking"} tweet`)
            }
        } catch (error) {
            console.error("Network error", error)
        }
    }
})

//Updates the UI based on like/unlike action.
function toggleLikeUI(likeButton, likeIcon, isLiked) {
    const likeCountElement = likeButton
    let currentLikeCount = parseInt(likeCountElement.textContent.trim(), 10) || 0

    if (isLiked) {
        likeButton.classList.remove("liked")
        likeIcon.classList.remove("fa-solid")
        likeIcon.classList.add("fa-regular")
        likeIcon.style.color = "#aaaaaa"
        likeCountElement.innerHTML = `<i class="fa-regular fa-heart like-tweet-icon"></i> ${Math.max(currentLikeCount - 1, 0)}`
    } else {
        likeButton.classList.add("liked")
        likeIcon.classList.remove("fa-regular")
        likeIcon.classList.add("fa-solid")
        likeIcon.style.color = "#e57373"
        likeCountElement.innerHTML = `<i class="fa-solid fa-heart like-tweet-icon"></i> ${currentLikeCount + 1}`
    }
}


//edit tweet (for power_users_only)
const editTweetModal = document.querySelector('.edit-tweet-modal')
const editTweetForm = editTweetModal.querySelector('.edit-tweet-form')

//show-close edit modal
document.addEventListener('click', async (event) => {
    if (event.target.classList.contains('edit-tweet-icon')){
        const tweetElement = event.target.closest('.tweet-card')
        if (tweetElement) {
            const tweetId = tweetElement.getAttribute('data-tweet-id')
            const tweetText = tweetElement.querySelector(".tweet-content").innerText.trim()
            const username = tweetElement.querySelector(".tweet-user-info strong").innerText.trim()
            const email = tweetElement.querySelector(".tweet-email").innerText.trim()
            const date = tweetElement.querySelector('.tweet-date').innerText.trim()

            editTweetModal.dataset.tweetId = tweetId
            editTweetModal.querySelector('.edit-tweet-text').value = tweetText
            editTweetModal.querySelector('.tweet-username').innerText = username
            editTweetModal.querySelector('.tweet-email').innerText = email
            editTweetModal.querySelector('.tweet-date').innerText = date
    
            editTweetModal.showModal()
            
        }
    }
})


document.querySelector('.close-edit-modal').addEventListener('click', () => {
    editTweetModal.close()
})

// tweet ediiting function
editTweetForm.addEventListener('submit', async(event) => {
    event.preventDefault();

    const tweetId = editTweetModal.dataset.tweetId;
    const updatedTweetText = editTweetModal.querySelector('.edit-tweet-text').value.trim();

    const data = JSON.stringify({
        tweet_content: updatedTweetText
    });

    try {
        const response = await fetch(`/tweets/api/tweet/${tweetId}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector("[name=csrfmiddlewaretoken]").value
            },
            body: data
        });
        if (response.ok) {
            editTweetModal.close()
            fetchCurrentUserTweets()
            openContentDialog(tweetId, 'tweet')
        }
    } catch (error) {
        console.log('Error updating tweet: ', error);
    }
});
