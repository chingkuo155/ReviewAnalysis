// /static/scripts.js
function post_review() {
    var formData = {
        "product_id": $("#product_id").val(),
        "rating": $("#rating").val(),
        "labels": $("#labels").val(),
        "reviews": $("#reviews").val()
    };
    $.ajax({
        url: "/add_review/",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify(formData),
        success: function(res) {
            alert("Review added successfully!");
            $("#reviewForm")[0].reset();
            loadCharts();
            loadAllReviews();
            loadRandomReviews();
        },
        error: function() {
            console.log("AJAX ERROR!!!");
        }
    });
}

function delete_review(index) {
    var index = $("#delete_index").val();
    $.ajax({
        url: "/delete_review/",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({index: index}),
        success: function(res) {
            alert("Review deleted successfully!");
            loadAllReviews();
        },
        error: function() {
            console.log("AJAX ERROR!!!");
        }
    });
}

function loadCharts() {
    $("#barChart").attr("src", "/bar_chart/");
    $("#wordCloud").attr("src", "/word_cloud/");
}

function loadAllReviews() {
    $.ajax({
        url: "/all_reviews/",
        method: "GET",
        success: function(res) {
            var reviewList = $("#allReviews");
            reviewList.empty();
            res.forEach(function(review) {
                var li = $("<li></li>");
                li.html(
                    "Index: " + review.index + "<br>" +
                    "Product ID: " + review.product_id + "<br>" +
                    "Rating: " + review.rating + "<br>" +
                    "Labels: " + review.labels + "<br>" +
                    "Reviews: " + review.reviews + "<br>" +
                    "Review Date: " + review.review_date + "<br>" +
                    "<button onclick='delete_review(" + review.index + ")'>Delete</button>"
                );
                reviewList.append(li);
            });
        },
        error: function() {
            console.log("AJAX ERROR!!!");
        }
    });
}

function loadRandomReviews() {
    $.ajax({
        url: "/random_reviews/",
        method: "GET",
        success: function(res) {
            var reviewList = $("#randomReviews");
            reviewList.empty();
            res.forEach(function(review) {
                var li = $("<li></li>");
                li.html(
                    "Product ID: " + review.product_id + "<br>" +
                    "Rating: " + review.rating + "<br>" +
                    "Labels: " + review.labels + "<br>" +
                    "Reviews: " + review.reviews + "<br>" +
                    "Review Date: " + review.review_date
                );
                reviewList.append(li);
            });
        },
        error: function() {
            console.log("AJAX ERROR!!!");
        }
    });
}

$(document).ready(function() {
    loadCharts();
    loadAllReviews();
    loadRandomReviews();
});
