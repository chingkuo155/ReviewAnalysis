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

function delete_review() {
    var index = $("#delete_index").val();
    $.ajax({
        url: "/delete_review/",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({index: index}),
        success: function(res) {
            alert("Review deleted successfully!");
            $("#deleteForm")[0].reset();
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

function loadAreaChart() {
    var startDate = $("#startDate").val();
    var endDate = $("#endDate").val();
    var areaChartUrl = `/area_chart/?start_date=${startDate}&end_date=${endDate}`;
    
    $.ajax({
        url: areaChartUrl,
        method: "GET",
        success: function() {
            $("#areaChart").attr("src", areaChartUrl);
        },
        error: function() {
            console.log("AJAX ERROR!!!");
        }
    });
}

function loadAllReviews() {
    $.ajax({
        url: "/all_reviews/",
        method: "GET",
        success: function(res) {
            var reviewList = $("#allReviews");
            reviewList.empty();
            res.forEach(function(review) {
                var fullReview = review.reviews;
                var shortReview = fullReview.length > 400 ? fullReview.substring(0, 400) + '...' : fullReview;
                var li = $("<li></li>");
                li.html(
                    "Index: " + review.index + "<br>" +
                    "Product ID: " + review.product_id + "<br>" +
                    "Rating: " + review.rating + "<br>" +
                    "Labels: " + review.labels + "<br>" +
                    "Reviews: <span class='review-text'>" + shortReview + "</span><br>" +
                    "Review Date: " + review.review_date + "<br>" +
                    "<button class='toggle-review' data-full='" + fullReview + "' data-short='" + shortReview + "'>顯示較多</button>"
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
                var fullReview = review.reviews;
                var shortReview = fullReview.length > 400 ? fullReview.substring(0, 400) + '...' : fullReview;
                var li = $("<li></li>");
                li.html(
                    "Product ID: " + review.product_id + "<br>" +
                    "Rating: " + review.rating + "<br>" +
                    "Labels: " + review.labels + "<br>" +
                    "Reviews: <span class='review-text'>" + shortReview + "</span><br>" +
                    "Review Date: " + review.review_date + "<br>" +
                    "<button class='toggle-review' data-full='" + fullReview + "' data-short='" + shortReview + "'>顯示較多</button>"
                );
                reviewList.append(li);
            });
        },
        error: function() {
            console.log("AJAX ERROR!!!");
        }
    });
}

$(document).on('click', '.toggle-review', function() {
    var button = $(this);
    var reviewText = button.siblings('.review-text');
    if (button.text() === '顯示較多') {
        reviewText.text(button.data('full'));
        button.text('顯示較少');
    } else {
        reviewText.text(button.data('short'));
        button.text('顯示較多');
    }
});

$(document).ready(function() {
    loadCharts();
    loadAllReviews();
    loadRandomReviews();
});
