console.log("This project sucks.")

function getSingleArticle(article, first = false) {
    var linkedTable = document.createElement('a')
    linkedTable.href = article.link

    //insert article title
    var table = document.createElement('table')
    var row = table.insertRow()
    var cell = row.insertCell()
    var title = document.createElement('h4')
    title.innerText = article.title
    title.className = "FirstArticleTitle"
    if (first == false) {
        title.className = "ArticleTitle"
        title.innerText = "• " + title.innerText
    }
    cell.innerHTML = title.outerHTML

    //insert article stamp
    var row = table.insertRow()
    var cell = row.insertCell()
    var stamp = document.createElement('h6')
    stamp.innerText = article.publisher + " • " + article.publish_ts
    stamp.className = "ArticleStamp"
    cell.innerHTML = stamp.outerHTML

    row.padding = 0
    linkedTable.innerHTML = table.outerHTML
    linkedTable.className = 'SingleArticleBlock'
    linkedTable.padding = 0
    return linkedTable
}
function getArticles(article_list, index) {
    var table = document.createElement('table')

    //insert leader article
    var row = table.insertRow()
    var cell = row.insertCell()
    cell.innerHTML = getSingleArticle(article_list[0], true).outerHTML
    

    //create an unordered list of follower articles
    var seeMore = document.createElement('a')
    seeMore.innerText = "See More"
    seeMore.className = "SeeMore"
    seeMore.href = "#NewsBlock" + String(index)
    seeMore.setAttribute("data-toggle", "collapse")


    var row = table.insertRow()
    var cell = row.insertCell()
    
    var divElement = document.createElement('div')
    divElement.setAttribute("id", "NewsBlock" + String(index))
    divElement.className = "collapse"
    var list = document.createElement('ul')
    list.className = "ArticleList"
    for (var i = 1; i < article_list.length; i++) {
        list.appendChild(getSingleArticle(article_list[i]), false)
    }
    divElement.innerHTML = list.outerHTML
    
    cell.appendChild(seeMore)
    cell.appendChild(divElement)

    table.className = 'ArticlesBlock'
    return table
}
function getThumbnail(article) {
    var imageWithLink = document.createElement('a')
    imageWithLink.href = article['article_list'][0].link
    var thumbnail = document.createElement('img')
    thumbnail.src = "data:image/PNG;base64," + article.thumbnail
    thumbnail.width = 150
    thumbnail.height = 150
    imageWithLink.appendChild(thumbnail)
    return imageWithLink
}
function getNewsBlock(news, index) {
    var table = document.createElement('table')
    table.className = 'NewsBlock'
    var row = table.insertRow()
    var cell = row.insertCell()
    cell.className = 'ArticleLinks'
    cell.innerHTML = getArticles(news['article_list'], index).outerHTML
    cell.setAttribute("width", "80%")
    var cell = row.insertCell()
    cell.innerHTML = getThumbnail(news).outerHTML
    cell.className = 'ThumbnailBlock'
    cell.setAttribute("width", "20%")
    return table
}
var result = {{ result | safe }}
var table = document.getElementById('ContentTable')
table.setAttribute("display", "block")
for (var i = 0; i < result.length; i++) {
    var row = table.insertRow()
    row.setAttribute("display", "block")
    row.insertCell().innerHTML = getNewsBlock(result[i], i).outerHTML
}