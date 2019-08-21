console.log("This project sucks.")

function getSingleArticle(article, first = false) {
    var linkedTable = document.createElement('a')
    console.log(article)
    linkedTable.href = article.link

    //insert article title
    var table = document.createElement('table')
    var row = table.insertRow()
    var cell = row.insertCell()
    var title = document.createElement('h2')
    title.innerText = article.title
    cell.innerHTML = title.outerHTML

    //insert article stamp
    var row = table.insertRow()
    var cell = row.insertCell()
    var stamp = document.createElement('h5')
    stamp.innerText = article.publisher + " ~ " + article.publish_ts
    cell.innerHTML = stamp.outerHTML

    //set class of article block
    if (first) {
        title.className = "FirstArticleTitle"
        stamp.className = "ArticleStamp"
    }
    else {
        title.className = "ArticleTitle"
        stamp.className = "ArticleStamp"
    }

    linkedTable.innerHTML = table.outerHTML
    return linkedTable
}
function getArticles(article_list) {
    var table = document.createElement('table')

    //insert leader article
    var row = table.insertRow()
    var cell = row.insertCell()
    console.log(article_list)
    cell.innerHTML = getSingleArticle(article_list[0]).outerHTML
    

    //create an unordered list of follower articles
    var row = table.insertRow()
    var cell = row.insertCell()
    var list = document.createElement('ul')
    for (var i = 1; i < article_list.length; i++) {
        list.appendChild(getSingleArticle(article_list[i]))
    }
    cell.innerHTML = list.outerHTML

    return table
}
function getThumbnail(article) {
    var imageWithLink = document.createElement('a')
    imageWithLink.href = article['article_list'][0].link
    var thumbnail = document.createElement('img')
    thumbnail.src = "data:image/PNG;base64," + article.thumbnail
    thumbnail.width = 100
    thumbnail.height = 100
    imageWithLink.appendChild(thumbnail)
}
function getNewsBlock(news) {
    var table = document.createElement('table')
    var row = table.insertRow()
    var cell = row.insertCell()
    cell.innerHTML = getArticles(news['article_list']).outerHTML
    var cell = row.insertCell()
    cell.innerHTML = getThumbnail(news).outerHTML
    return table
}
var result = {{ result | safe }}
var table = document.createElement('table')
console.log(result.length)
for (var i = 0; i < result.length; i++) {
    table.insertRow().insertCell().innerHTML = getNewsBlock(result[i]).outerHTML
}
document.getElementById('ContentBlock').innerHTML = outerHTML
