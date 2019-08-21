console.log("This project sucks.")

function getSingleArticle(article, first = false) {
    var linkedTable = document.createElement('a')
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
    var cell = table.insertCell()
    var stamp = document.createElement('h5')
    stamp.innerText = article.publisher + " ~ " + article.time
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
function getArticles(news) {
    var table = document.createElement('table')

    //insert leader article
    var row = table.insertRow()
    var cell = row.insertCell()
    cell.innerHTML = getSingleArticle(news[0]).outerHTML
    

    //create an unordered list of follower articles
    var row = table.insertRow()
    var cell = table.insertCell()
    var list = document.createElement('ul')
    for (var i = 1; i < news.length; i++) {
        list.appendChild(getSingleArticle(news[i]))
    }
    cell.innerHTML = list.outerHTML

    return table
}
function getThumbnail(article) {
    var imageWithLink = document.createElement('a')
    imageWithLink.href = article[0].link
    var thumbnail = document.createElement('img')
    thumbnail.src = "data:image/PNG;base64," + article.thumbnail
    thumbnail.width = 100
    thumbnail.height = 100
    imageWithLink.appendChild(thumbnail)
}
function getNewsBlock(article) {
    var table = document.createElement('table')
    var row = table.insertRow()
    var cell = row.insertCell()
    cell.innerHTML = getArticles(article).outerHTML
    var cell = row.insertCell()
    cell.innerHTML = getThumbnail(article).outerHTML
    return table
}
var result = {{ result | safe }}
var table = document.createElement('table')
console.log(result.length)
for (var i = 0; i < result.length; i++) {
    table.insertRow().insertCell().innerHTML = getNewsBlock(result[i]).outerHTML
}
document.getElementById('ContentBlock').innerHTML = outerHTML
