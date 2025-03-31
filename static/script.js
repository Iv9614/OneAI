function fetchNewsList() {
    $.ajax({
        url: 'http://127.0.0.1:8000/v1/crawlers/list/', 
        method: 'GET',
        success: function(response) {
            const newsData = response.data;
            let newsHtml = '';

            newsData.forEach(news => {
                // 格式化時間（只顯示日期和時間部分）
                const newsTime = new Date(news.news_time).toLocaleString('zh-TW', {
                    year: 'numeric',
                    month: '2-digit',
                    day: '2-digit',
                    hour: '2-digit',
                    minute: '2-digit'
                });

                newsHtml += `
                    <div class="col-md-4 mb-3">
                        <div class="card news-card">
                            <div class="card-body">
                                <h5 class="card-title">${news.title}</h5>
                                <p class="card-text">${newsTime}</p>
                                <a href="${news.link}" target="_blank" class="btn btn-primary">查看詳情</a>
                            </div>
                        </div>
                    </div>
                `;
            });
            $('#news-list').html(newsHtml);
        },
        error: function(error) {
            $('#news-list').html('<p class="text-danger">無法載入新聞列表</p>');
            console.error('Error fetching news list:', error);
        }
    });
}
