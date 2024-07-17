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

function loadAllReviews() {
    $.ajax({
        url: "/all_reviews/",
        method: "GET",
        success: function(res) {
            var reviewList = $("#allReviews");
            reviewList.empty();
            res.forEach(function(review) {
                var li = $("<li></li>");
                var fullReview = review.reviews;
                var shortReview = truncateReview(fullReview);
                li.html(
                    "Index: " + review.index + "<br>" +
                    "Product ID: " + review.product_id + "<br>" +
                    "Rating: " + review.rating + "<br>" +
                    "Labels: " + review.labels + "<br>" +
                    "Reviews: <div class='review-text-container'>" +
                        "<p class='review-text short-review'>" + shortReview + "</p>" +
                        "<p class='review-text full-review d-none'>" + fullReview + "</p>" +
                    "</div>" +
                    "Review Date: " + review.review_date + "<br>" +
                    "<button class='toggle-review d-none'>顯示更多</button>"
                );
                reviewList.append(li);
            });
            toggleReviewButton();
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
                var fullReview = review.reviews;
                var shortReview = truncateReview(fullReview);
                li.html(
                    "Product ID: " + review.product_id + "<br>" +
                    "Rating: " + review.rating + "<br>" +
                    "Labels: " + review.labels + "<br>" +
                    "Reviews: <div class='review-text-container'>" +
                        "<p class='review-text short-review'>" + shortReview + "</p>" +
                        "<p class='review-text full-review d-none'>" + fullReview + "</p>" +
                    "</div>" +
                    "Review Date: " + review.review_date + "<br>" +
                    "<button class='toggle-review d-none'>顯示更多</button>"
                );
                reviewList.append(li);
            });
            toggleReviewButton();
        },
        error: function() {
            console.log("AJAX ERROR!!!");
        }
    });
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

function truncateReview(review) {
    var div = $("<div>").html(review);
    var text = div.text();
    var lines = text.split(/\r\n|\r|\n/).length;
    return lines > 3 ? text.split(/\r\n|\r|\n/).slice(0, 3).join(" ") + '...' : text;
}

function toggleReviewButton() {
    $(".review-text-container").each(function() {
        var container = $(this);
        var shortReview = container.find(".short-review");
        var fullReview = container.find(".full-review");

        if (shortReview.height() < fullReview.height()) {
            container.siblings(".toggle-review").removeClass("d-none");
        }
    });
}

$(document).on('click', '.toggle-review', function() {
    var button = $(this);
    var shortReview = button.siblings('.review-text-container').find('.short-review');
    var fullReview = button.siblings('.review-text-container').find('.full-review');
    if (shortReview.hasClass('d-none')) {
        shortReview.removeClass('d-none');
        fullReview.addClass('d-none');
        button.text('顯示更多');
    } else {
        shortReview.addClass('d-none');
        fullReview.removeClass('d-none');
        button.text('顯示較少');
    }
});

$(document).ready(function() {
    loadCharts();
    loadAllReviews();
    loadRandomReviews();
    loadAreaChart()

    $('#toggleReviewsBtn').click(function() {
        $('#allReviewsContainer').toggle();
    });
});
