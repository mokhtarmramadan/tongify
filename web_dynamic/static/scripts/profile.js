$(document).ready(init);
// window.onload = function() {
//     // Function to get a cookie by name
//     function getCookie(name) {
//         const value = `; ${document.cookie}`;
//         const parts = value.split(`; ${name}=`);
//         if (parts.length === 2) return parts.pop().split(';').shift();
//     }

//     const token = getCookie('token');
  
// }

let userPosts = [];
function init() {
    const token = Cookies.get('token');
    console.log(token);
    let joinDate = $("#join_date").text();
    joinDate = joinDate.substring(0, 21);
    $("#join_date").text(joinDate);

    $("#edit-bio").click(function() {
        $("#bio-post-form-overlay").toggle();
        $("#bio-content-feild").val(bio);
    });
    $("#create-bio-btn").click(function() {
        const updatedUserBio = {"bio": $("#bio-content-feild").val()};
        $.ajax({
            url: `http://192.168.1.18:5050/api/v1/users/${userId}`,
            type: 'PUT',
            data: JSON.stringify(updatedUserBio),
            contentType: 'application/json',
            success: function(response, textStatus, jqXHR) {
                console.log("Full Response:", response, textStatus, jqXHR);  // Log the full response
                if (jqXHR.status === 200) {  // Check the jqXHR status for 200
                    console.log("done");
                    location.reload();
                } else {
                    console.error("Error:", response.statusText);
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error("Error:", textStatus, errorThrown);
            }
        });
    });


    $("#bio-cancel-form-btn").click(function () {
        $("#bio-post-form-overlay").toggle();
    });

    $("#edit-find-me").click(function() {
        $("#update-find-me-form-overlay").toggle();
    });

    $("#find-me-cancel-form-btn").click(function() {
        $("#update-find-me-form-overlay").toggle();
    });

    $(".create_post_btn").click(function() {
        $("#create-post-form-overlay").toggle();
    }); 

    $("#cancel-form-btn").click(function() {
        $("#create-post-form-overlay").toggle();
    });
    $("#cancel-update-form-btn").click(function() {
        $("#update-post-form-overlay").toggle();
    });
    
    $("#create-form-btn").click(function() {
        var title = $(".post_feild").val();
        var content = $("#create-content-feild").val();

        if (title.length >= 35) {
            $(".text-limit-title").css('display', 'block');
        } else if (content.length >= 140) {
            $(".text-limit-content").css('display', 'block');
        }
        else {
            $(".text-limit-title").css('display', 'none');
            $(".text-limit-content").css('display', 'none');
            const data = {
                "title": title,
                "content": content,
                "user_id": userId
            };
            $.ajax({
                url: `http://192.168.1.18:5050/api/v1/users/${userId}/posts`,
                type: 'POST',
                data: JSON.stringify(data),
                contentType: 'application/json',
                success: function(response) {
                    if (response.status === 201) {
                        console.log("done");
                        location.reload();
                        // Try to open the post section afterwards

                    } else {
                        console.error("Error:", response.statusText);
                    }
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.error("Error:", textStatus, errorThrown);
                }
            });
        }
    });

    let requested = false;

    $(".profile_posts_button").click(function() {
        // when the load posts icon is clicked 
        if ($(".profile_posts_image").hasClass("open")) {
            // If it's clicked to close
            $(".profile_posts_image").removeClass("open");
            $(".profile_posts_image").attr("src", "../static/images/greater-than-symbol.png");
            $(".posts").addClass("hide");
        } else {
            // If it's clicked to open
            $(".profile_posts_image").attr("src", "../static/images/down-greater-than.png");
            $(".profile_posts_image").addClass("open");
            $(".posts").removeClass("hide");

            // Render posts by that user
            if (requested === false) {
                // Send request has been sent before don't send more
                $.ajax({
                    url: `http://192.168.1.18:5050/api/v1/users/${userId}/posts`,
                    type: 'GET',
                    headers: {
                        'Authorization': `${token}`
                    },
                success: function(posts, textStatus) {
                    // Send a get request to this end-point to retrieve posts by user
                    if (textStatus == 'success') {
                        requested = true; // Set flag
                        posts.forEach(function(post) {
                            let postDate = post.created_at;
                            postDate = postDate.substring(0, 7);
                            const postHTML = `
                                <div class="media-body profile">
                                    <div class="media-body profile_post">
                                        <div class="article-metadata">
                                            <img class="rounded-circle post_image" src="${userImage}">
                                            <a class="mr-2" id="post_username" href="#">${userName}</a>
                                            <small class="text-muted" id="post_date">${postDate}</small>
                                        </div>
                                        <div class="actual_post">
                                            <h4 class="article-title">${post.title}</h4>
                                            <p class="article-content">${post.content}</p>
                                        </div>
                                        <div class="button-container d-flex gap-2 justify-content-end"> 
                                            <div name=${post.id} class="btn btn-primary profile_btn update-btn">Update</div>
                                            <div name=${post.id} class="btn btn-primary profile_btn danger-button delete-btn">Delete</div>
                                        </div>
                                    </div>
                                </div>`;
                                userPosts[post.id] = {'title': post.title, 'content': post.content};
                            $(".posts").append(postHTML);
                        });
                    }
                        let deleteTargetPostId = '';
                        $(".delete-btn").click(function() {
                            $("#delete-post-form-overlay").toggle();
                            deleteTargetPostId = $(this).attr('name');
                        });

                        $("#delete-form-btn").click(function() {
                            $.ajax({
                                url: `http://192.168.1.18:5050/api/v1/users/${userId}/posts/${deleteTargetPostId}`,
                                type: 'DELETE',
                                success: function(response) {
                                    location.reload();

                                }
                            });
                        });

                        $("#cancel-delete-form-btn").click(function() {
                            $("#delete-post-form-overlay").toggle();
                        });


                        let updatePostId = '';
                        $(".update-btn").click(function(){
                            $("#update-post-form-overlay").toggle();
                            updatePostId = $(this).attr('name');
                            const thisPost = userPosts[updatePostId];
                            const postTitle = thisPost.title;
                            const postContent = thisPost.content;
                            $("#update-title-feild").val(postTitle);
                            $("#update-content-feild").val(postContent);
                        });
                        $("#update-form-btn").click(function() {
                            const postData = {'title': $("#update-title-feild").val(), 'content': $("#update-content-feild").val()}
                            $.ajax({
                                url: `http://192.168.1.18:5050/api/v1/users/${userId}/posts/${updatePostId}`,
                                type: 'PUT',
                                data: JSON.stringify(postData),
                                contentType: 'application/json',
                                success: function(response) {
                                    location.reload();
                                },
                            });

                        });
                    }
                });
            }
        }
    });
}