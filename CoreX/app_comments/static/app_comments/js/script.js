const closeTweetModal = document.querySelector('.close-tweet-modal')

// Opening-closing modal
closeTweetModal.addEventListener('click', () => {
    const tweetDialog = document.querySelector('.individual-tweet-modal')
    document.body.classList.remove("modal-open")
    document.querySelector(".individual-tweet-modal").style.display = "none"
    tweetDialog.close() 
})

document.addEventListener('click', async (event) => {
    if (event.target.closest('.tweet-content')) {
        const tweetElement = event.target.closest('.tweet-card')
        if (tweetElement) {
            const tweetId = tweetElement.getAttribute('data-tweet-id')
            await openContentDialog(tweetId, 'tweet')
        }
    }
    if (event.target.closest('.comment-container')) {
        const commentElement = event.target.closest('.comment')
        if (commentElement) {
            const commentId = commentElement.getAttribute('data-comment-id')
            await openContentDialog(commentId, 'comment')
        }
    }
})

// Function to open content dialog (tweet or comment)
async function openContentDialog(contentId, type) {
    try {
        const response = await fetch(`/${type}s/api/${type}/${contentId}`)
        const contentData = await response.json()

        const contentDialog = document.querySelector('.individual-tweet-modal')
        contentDialog.dataset.contentId = contentId
        contentDialog.dataset.contentType = type

        if (type === 'tweet') {
            contentDialog.querySelector('.tweet-username').textContent = contentData.author.username
            contentDialog.querySelector('.tweet-email').textContent = `@${contentData.author.email.split('@')[0]}`
            contentDialog.querySelector('.tweet-date').textContent = new Date(contentData.created_at).toLocaleString()
            contentDialog.querySelector('.tweet-text').textContent = contentData.tweet_content
            contentDialog.querySelector('.tweet-media').innerHTML = renderMedia(contentData.media)
        } else if (type === 'comment') {
            contentDialog.querySelector('.tweet-username').textContent = contentData.author.username
            contentDialog.querySelector('.tweet-email').textContent = `@${contentData.author.email.split('@')[0]}`
            contentDialog.querySelector('.tweet-date').textContent = new Date(contentData.created_at).toLocaleString()
            contentDialog.querySelector('.tweet-text').textContent = contentData.comment_content
            contentDialog.querySelector('.tweet-media').innerHTML = '' //currently not adding media in comments later on i will figure it out (maybe adding 1 more column in comment model)
        }

        await loadComments(contentId, type)
        document.body.classList.add("modal-open")
        document.querySelector(".individual-tweet-modal").style.display = "block"   
        contentDialog.showModal()
    } catch (error) {
        console.error('Error:', error)
    }
}

// Function to load comments or replies
async function loadComments(contentId, type) {
    try {
        let response
        if (type==='tweet')
            {
            response = await fetch(`/comments/api/comment/${type}/${contentId}/`)
            }
        else{
            response= await fetch(`/comments/api/comment/${contentId}/`)
        }
        const data = await response.json()
        const commentList = document.querySelector('.comments-list')
        commentList.innerHTML = ``
        
        let dataset
        if(data.comments){
            dataset = data.comments
        }
        else{
            dataset = data.replies
        }

        dataset.forEach(comment => {
            const commentElement = document.createElement('div')
            commentElement.classList.add('comment')
            commentElement.setAttribute('data-comment-id', comment.id)
            commentElement.innerHTML = `
                <div class='comment-header'>
                    <img src="https://abs.twimg.com/sticky/default_profile_images/default_profile_400x400.png" alt="Profile" class="profile-pic">
                    <div class='comment-user-info'>
                        <strong>${comment.author.username}</strong>
                        <div class='comment-user-detail'>@${comment.author.email.split('@')[0]}</div>
                        <div class='comment-user-detail'>${new Date(comment.created_at).toLocaleString()}</div>
                    </div>
                </div>
                <div class='comment-container'>${comment.comment_content}</div>   
            `
            commentList.appendChild(commentElement)
        })
    } catch (error) {
        console.error('Error loading comments:', error)
    }
}

//posting a tweet reply
document.addEventListener('click', (event)=>{
    if (event.target.classList.contains('tweet-reply')){
        event.preventDefault()
        postReply()
    }
})

async function postReply(){
    const reply = document.querySelector('.reply-text')
    const replyText = reply.value.trim()
    if (!replyText){
        reply.placeholder = "What's on your mind?"
        reply.focus()
        return
    }

    reply.value = ''
    const parentCommentElement = document.querySelector('.individual-tweet-modal')
    const contentId = parentCommentElement.dataset.contentId
    const contentType = parentCommentElement.dataset.contentType

    const parentId = contentType === 'comment' ? contentId : null

    const url = contentType === 'tweet'
         ? `/comments/api/comment/tweet/${contentId}/create/`
         : `/comments/api/comment/${contentId}/replies/`

    try{
        const replyData = JSON.stringify({
            comment_content : replyText,
            parent_id: parentId
        })

        const response = await fetch(url, {
            method: 'POST',
            headers:{
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector("[name=csrfmiddlewaretoken]").value
            },
            body:replyData
        })

        if (response.ok){
            const data = await response.json()
            console.log("Comment posted", data)
            await loadComments(contentId, contentType)
        }
        else{
            console.log("Error posting comment")
        }
    }
    catch(error){
        console.log("Error posting: ", error)
    }

}