console.log("hello")

function insertIntoTable(table, value) {
table.insertRow().insertCell().innerHTML = value.outerHTML
}
function getArticle(article) {
var table = document.createElement('table')

var thumbnail = document.createElement('img')
thumbnail.src = "data:image/JPG;base64," + article.thumbnail
insertIntoTable(table, thumbnail)

var title = document.createElement('h3')
title.innerText = article.title
insertIntoTable(table, title)

var summary = document.createElement('p')
summary.innerText = article.summary
insertIntoTable(table, summary)
return table
}
function getLinks(article) {
var table = document.createElement('table')

var parity = 0
var currentRow = null
for (var i = 0; i < article.links.length; i++) {
if (parity == 0) {
currentRow = table.insertRow()
}
var currentCell = currentRow.insertCell()
var imageLink = document.createElement('a')
imageLink.href = article.links[i]

var image = new Image()
image.src = "data:image/PNG;base64," + article.logos[i]
image.width = 50
image.height= 50

imageLink.appendChild(image)
currentCell.innerHTML = imageLink.outerHTML
parity = parity ^ 1
}

return table
}
function getArticleBlock(article) {
var table = document.createElement('table')
var row = table.insertRow()
row.insertCell().innerHTML = getArticle(article).outerHTML
row.insertCell().innerHTML = getLinks(article).outerHTML
return table
}
var result = {{ result | safe }}
var table = document.createElement('table')
for (var i = 0; i < 3; i++) {
var row = table.insertRow()
for (var j = 0; j < 3; j++) {
var idx = i * 3 + j
row.insertCell().innerHTML = getArticleBlock(result[idx]).outerHTML
}
}
document.getElementsByTagName('body')[0].appendChild(table)
