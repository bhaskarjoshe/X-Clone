document.addEventListener("DOMContentLoaded", function () {
    fetchTweets()
    document.getElementById("load-more-btn").addEventListener("click", loadMoreTweets)
})

let currentPage = 1


//fetching tweets
async function fetchTweets(page = 1, url = allTweetsApiUrl) {
    try {
        const urlWithPageNo = `${url}?page=${page}`
        const response = await fetch(urlWithPageNo)
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`)
        }
        const data = await response.json()

        const tweetContainer = document.getElementById("tweet-container")
        if (page === 1) {
            tweetContainer.innerHTML = ""
        }

        data.results.forEach(tweet => {
            const tweetElement = document.createElement("div")
            tweetElement.classList.add("tweet-card")
            tweetElement.innerHTML = `
                <div class="tweet-header">
                    <img src="https://abs.twimg.com/sticky/default_profile_images/default_profile_400x400.png" alt="Profile" class="profile-pic">
                    <div class="tweet-user-info">
                        <strong>${tweet.author.username}</strong> 
                        <span class="tweet-email">@${tweet.author.email.split('@')[0]}</span>
                        <span class="tweet-date">${new Date(tweet.created_at).toLocaleString()}</span>
                    </div>
                </div>
                <div class="tweet-content">
                    ${tweet.tweet_content}
                    ${renderMedia(tweet.media)}
                </div>
                <div class="tweet-actions">
                    <span class="tweet-action"><i class="fa-regular fa-comment"></i> ${tweet.comments.length}</span>
                    <span class="tweet-action"><i class="fa-solid fa-retweet"></i>0</span>
                    <span class="tweet-action"><i class="fa-regular fa-heart"></i> ${tweet.likes.length}</span>
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
    if (forYouToggle.classList.contains('navbar-center-active')) {
        await fetchTweets(currentPage, allTweetsApiUrl)
    } else if (followingToggle.classList.contains('navbar-center-active')) {
        await fetchTweets(currentPage, allFollowingTweetsApiUrl)
    }
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


//to toggle b/w for-you and following
const forYouToggle = document.querySelector('.for-you')
const followingToggle = document.querySelector('.following')

forYouToggle.addEventListener('click', () => {
    forYouToggle.classList.add('navbar-center-active')
    followingToggle.classList.remove('navbar-center-active')
    currentPage = 1
    fetchTweets(1, allTweetsApiUrl)
    document.getElementById('load-more-btn').style.display = "block"
})

followingToggle.addEventListener('click', () => {
    forYouToggle.classList.remove('navbar-center-active')
    followingToggle.classList.add('navbar-center-active')
    currentPage = 1
    fetchTweets(1, allFollowingTweetsApiUrl)
    document.getElementById('load-more-btn').style.display = "block"
})


//media icon for tweets (to be modified later on)
function triggerFileInput() {
    document.getElementById('media-input').click()
}

let selectedFile = null
const allowedMediaTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'video/mp4', 'video/webm', 'video/ogg']

function handleFileChange(event) {
    const file = event.target.files[0]

    if (!allowedMediaTypes.includes(file.type)) {
        event.target.value = ''
        selectedFile = null
        return
    }

    selectedFile = file
}


// posting a tweet
async function postTweet() {
    const tweetTextarea = document.querySelector('textarea[name="tweet"]')
    const tweetText = tweetTextarea.value.trim()

    if (!tweetText) {
        tweetTextarea.placeholder = "Enter something...."
        tweetTextarea.classList.add("error")
        return
    }

    tweetTextarea.addEventListener("input", () => {
        tweetTextarea.classList.remove("error")
    })

    const formData = new FormData()
    formData.append('tweet_content', tweetText)

    if (selectedFile) {
        formData.append('media', selectedFile)
    }

    try {
        const response = await fetch(postTweetUrl, {
            method: "POST",
            headers: {
                'X-CSRFToken': document.querySelector("[name=csrfmiddlewaretoken]").value
            },
            body: formData
        })
        await response.json()
        fetchTweets(1, allTweetsApiUrl)
        tweetTextarea.value = ""
        document.getElementById('media-input').value = ''
    } catch (error) {
        console.log(error)
    }
}


//media file with tweet
async function uploadMedia(postTweetMediaUrl, selectedFile) {
    const formData = new FormData()
    formData.append('file', selectedFile, selectedFile.name)

    try {
        const response = await fetch(postTweetMediaUrl, {
            method: "POST",
            headers: {
                'X-CSRFToken': document.querySelector("[name=csrfmiddlewaretoken]").value
            },
            body: formData
        })
        const mediaData = await response.json()

        if (response.ok) {
            console.log("Media uploaded successfully: ", mediaData)
        } else {
            console.log("Media upload failed: ", mediaData)
        }
    } catch (error) {
        console.log(error)
    }
}


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
