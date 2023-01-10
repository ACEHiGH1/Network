// JavaScript function that shows and sends the new changes in the post to the editPost API.
function savepost(postId) {
    console.log("Button was clicked");
    const content = document.querySelector(`#PostContentTextArea`).value;
    const postID = postId
    document.querySelector(`#post${postId}details`).innerHTML = `
    <p class="mb-1">${content}</p>
    `;

    document.querySelector(`#edit${postId}`).style.display = 'block';
    document.querySelector(`#like${postId}`).style.display = 'block';

    console.log("go here")

    fetch(`/editPost/${postId}`, {
        method: 'POST',
        body: JSON.stringify({
            content: content,
            id: postID,
        })
    })
        .then(response => response.json())
        .then(result => {
            // Print result
            console.log(result);
        });

}
// Javascript function that shows the current content of the post when edited in a textarea.
function editPost(postId) {

    fetch(`editPost/${postId}`)
        .then(response => response.json())
        .then(post => {
            console.log(post.content);

            document.querySelector(`#post${post.id}details`).innerHTML = `
                <textarea class="form-control" id="PostContentTextArea"></textarea>
                <button type="button" class="btn btn-primary" onclick = "savepost(${postId})" id = "savePost"> Save </button>
            `;

            document.querySelector(`#PostContentTextArea`).value = post.content;
            document.querySelector(`#edit${post.id}`).style.display = 'none';
            document.querySelector(`#like${post.id}`).style.display = 'none';
        })
}
// JS function that asynchronously likes a post and then fetches the data to the likePost API in the backend
function likePost(postId) {
    fetch(`editPost/${postId}`)
        .then(response => response.json())
        .then(post => {
            document.getElementById(`post${post.id}likes`).innerHTML = `
            <small class="text-primary" id = "${post.id}likes"> ${post.likes + 1} Likes</small>
            `;
            document.getElementById(`unlike${post.id}`).style.display = 'block';
            document.getElementById(`like${post.id}`).style.display = 'none';
            console.log(1);
            fetch(`/likePost/${postId}`, {
                method: 'POST',
                body: JSON.stringify({
                    id: postId
                })
            })
                .then(response => response.json())
                .then(result => {
                    // Print result
                    console.log(result);
                });
        })


}
// JS function that asynchronously unlikes a post and then fetches the data to the unlikePost API in the backend
function unlikePost(postId) {
    fetch(`editPost/${postId}`)
        .then(response => response.json())
        .then(post => {
            document.getElementById(`post${post.id}likes`).innerHTML = `
            <small class="text-primary" id = "${post.id}likes"> ${post.likes - 1}  Likes</small>
            `;
            document.getElementById(`unlike${post.id}`).style.display = 'none';
            document.getElementById(`like${post.id}`).style.display = 'block';
            fetch(`/unlikePost/${postId}`, {
                method: 'POST',
                body: JSON.stringify({
                    id: postId
                })
            })
                .then(response => response.json())
                .then(result => {
                    // Print result
                    console.log(result);
                });
        })

}

