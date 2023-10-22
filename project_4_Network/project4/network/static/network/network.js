
document.addEventListener('click', event => {

    const element = event.target;
    if (element.id === 'edit-post') {
        const parent = element.parentElement.parentElement;
        const content = parent.querySelector('.content');
        let postContent = content.innerText;

        let cancle = document.createElement('a');
        cancle.id = 'cancle-edit';
        cancle.className = 'text-danger font-weight-bold';
        cancle.innerText = 'Cancel';
        element.replaceWith(cancle)

        cancle.onclick = () => {
            content.innerText = postContent;
            parent.querySelector('#cancle-edit').replaceWith(element);
        }

        content.innerHTML = `<div class="form-group">
                                <textarea id="textarea" class="form-control" name="content" rows="5" required></textarea>
                                <button id="save-edited-post" type="submit" class="btn btn-primary mt-2">Save</button>
                            </div>`;

        parent.querySelector('#textarea').value = postContent;
        parent.querySelector('#save-edited-post').addEventListener('click', () => edit(parent));
    };

    function edit(parent) {
        fetch('/edit', {
            method: 'POST',
            body: JSON.stringify({
                id: parent.querySelector('#post-id').innerText,
                content: parent.querySelector('#textarea').value
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            parent.querySelector('.content').innerText = parent.querySelector('#textarea').value;
            parent.querySelector('#cancle-edit').replaceWith(element);
        })
    }

    if (element.id === 'unfollow') {
        fetch("/change-follow", {
            method: 'POST',
            body: JSON.stringify({
                profile_id: element.dataset.userid,
                value: 'unfollow'
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);

            const follow = document.createElement('button');
            follow.id = 'follow';
            follow.className = 'btn btn-outline-primary mt-2';
            follow.innerText = 'Follow';
            follow.dataset.userid = element.dataset.userid;

            element.replaceWith(follow);

            followers = parseInt(document.querySelector('#followers').innerText);
            decreased = followers - 1;
            document.querySelector('#followers').innerText = decreased + " " + "Followers";
        })
    };

    if (element.id === 'follow') {
        fetch("/change-follow", {
            method: 'POST',
            body: JSON.stringify({
                profile_id: element.dataset.userid,
                value: 'follow'
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);

            const unfollow = document.createElement('button');
            unfollow.id = 'unfollow';
            unfollow.className = 'btn btn-outline-danger mt-2';
            unfollow.innerText = 'Unfollow';
            unfollow.dataset.userid = element.dataset.userid;

            element.replaceWith(unfollow);

            followers = parseInt(document.querySelector('#followers').innerText);
            increased = followers + 1;
            document.querySelector('#followers').innerText = increased + " " + "Followers";
        })
    };

    if (element.id == 'like-btn') {
        fetch("/change-like", {
            method: 'POST',
            body: JSON.stringify({
                value: element.dataset.value,
                post_id: element.dataset.postid
            })
        })
        .then(response => {
            if (!response.ok) {
                element.nextElementSibling.nextElementSibling.style.display = 'inline';
                throw new Error('Need to login');
            }

            return response.json();
        })
        .then(result => {
            console.log(result);

            if (element.dataset.value === 'like') {
                const unlike = document.createElement('a');
                unlike.id = 'like-btn';
                unlike.dataset.postid = element.dataset.postid;
                unlike.dataset.value = 'unlike';
                unlike.innerText = '🤍';

                let likes = parseInt(element.nextElementSibling.innerText);
                likes--;
                element.nextElementSibling.innerText = likes;

                element.replaceWith(unlike);
            }

            else if (element.dataset.value === 'unlike') {
                const like = document.createElement('a');
                like.id = 'like-btn';
                like.dataset.postid = element.dataset.postid;
                like.dataset.value = 'like';
                like.innerText = '❤️';

                let likes = parseInt(element.nextElementSibling.innerText);
                likes++;
                element.nextElementSibling.innerText = likes;

                element.replaceWith(like);
            }
        })
        .catch(error => {
            console.error("Error:", error);
        })
    }
})
