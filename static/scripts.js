// /static/scripts.js

// /static/scripts.js

const API_ENDPOINTS = {
    ADD_REVIEW: '/add_review/',
    DELETE_REVIEW: '/delete_review/',
    ALL_REVIEWS: '/all_reviews/',
    RANDOM_REVIEWS: '/random_reviews/',
    BAR_CHART: '/bar_chart/',
    WORD_CLOUD: '/word_cloud/',
    AREA_CHART: '/area_chart/'
};

async function postReview() {
    const formData = {
        product_id: $("#product_id").val(),
        rating: parseInt($("#rating").val()),
        labels: $("#labels").val(),
        reviews: $("#reviews").val()
    };

    try {
        const response = await $.ajax({
            url: API_ENDPOINTS.ADD_REVIEW,
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify(formData)
        });

        alert("評論新增成功！");
        $("#reviewForm")[0].reset();
        await Promise.all([loadCharts(), loadAllReviews(), loadRandomReviews()]);
    } catch (error) {
        console.error("新增評論時發生錯誤:", error);
        alert("新增評論失敗，請稍後再試。");
    }
}

async function deleteReview() {
    const index = parseInt($("#delete_index").val());

    try {
        const response = await $.ajax({
            url: API_ENDPOINTS.DELETE_REVIEW,
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({ index })
        });

        alert("評論刪除成功！");
        $("#deleteForm")[0].reset();
        await loadAllReviews();
    } catch (error) {
        console.error("刪除評論時發生錯誤:", error);
        alert("刪除評論失敗，請稍後再試。");
    }
}

async function loadAllReviews() {
    try {
        const reviews = await $.ajax({
            url: API_ENDPOINTS.ALL_REVIEWS,
            method: "GET"
        });

        const reviewList = $("#allReviews");
        reviewList.empty();

        reviews.forEach(review => {
            const li = createReviewElement(review);
            reviewList.append(li);
        });

        toggleReviewButton();
    } catch (error) {
        console.error("載入所有評論時發生錯誤:", error);
    }
}

async function loadRandomReviews() {
    try {
        const reviews = await $.ajax({
            url: API_ENDPOINTS.RANDOM_REVIEWS,
            method: "GET"
        });

        const reviewList = $("#randomReviews");
        reviewList.empty();

        reviews.forEach(review => {
            const li = createReviewElement(review, false);
            reviewList.append(li);
        });

        toggleReviewButton();
    } catch (error) {
        console.error("載入隨機評論時發生錯誤:", error);
    }
}

function createReviewElement(review, includeIndex = true) {
    const li = $("<li></li>");
    const fullReview = review.reviews;
    const shortReview = truncateReview(fullReview);

    let reviewContent = "";
    if (includeIndex) {
        reviewContent += `索引: ${review.index}<br>`;
    }
    reviewContent += `
        產品 ID: ${review.product_id}<br>
        評分: ${review.rating}<br>
        標籤: ${review.labels}<br>
        評論: <div class='review-text-container'>
            <p class='review-text short-review'>${shortReview}</p>
            <p class='review-text full-review d-none'>${fullReview}</p>
        </div>
        評論日期: ${review.review_date}<br>
        <button class='toggle-review d-none'>顯示更多</button>
    `;

    li.html(reviewContent);
    return li;
}

async function loadAreaChart() {
    const startDate = $("#startDate").val();
    const endDate = $("#endDate").val();
    const areaChartUrl = `${API_ENDPOINTS.AREA_CHART}?start_date=${startDate}&end_date=${endDate}`;
    
    try {
        await $.ajax({
            url: areaChartUrl,
            method: "GET"
        });
        $("#areaChart").attr("src", areaChartUrl);
    } catch (error) {
        console.error("載入面積圖時發生錯誤:", error);
        alert("載入面積圖失敗，請稍後再試。");
    }
}

function truncateReview(review) {
    const div = $("<div>").html(review);
    const text = div.text();
    const lines = text.split(/\r\n|\r|\n/);
    return lines.length > 3 ? lines.slice(0, 3).join(" ") + '...' : text;
}

function toggleReviewButton() {
    $(".review-text-container").each(function() {
        const container = $(this);
        const shortReview = container.find(".short-review");
        const fullReview = container.find(".full-review");

        if (shortReview.height() < fullReview.height()) {
            container.siblings(".toggle-review").removeClass("d-none");
        }
    });
}

$(document).ready(function() {
    loadCharts();
    loadAllReviews();
    loadRandomReviews();
    loadAreaChart();

    $('#toggleReviewsBtn').on('click', function() {
        $('#allReviewsContainer').toggle();
    });

    $(document).on('click', '.toggle-review', function() {
        const button = $(this);
        const container = button.siblings('.review-text-container');
        const shortReview = container.find('.short-review');
        const fullReview = container.find('.full-review');
        
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

    $('#reviewForm').on('submit', function(e) {
        e.preventDefault();
        postReview();
    });

    $('#deleteForm').on('submit', function(e) {
        e.preventDefault();
        deleteReview();
    });

    $('#areaChartForm').on('submit', function(e) {
        e.preventDefault();
        loadAreaChart();
    });
});
