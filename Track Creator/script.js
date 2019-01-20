var mousePos = []
var innerWall = []
var outerWall = []

var currentWall = outerWall
var currentWallName = 'outerWall'

var currentWallClosed = false
innerWallClosed = false
outerWallClosed = false

var ctrl = false
var shift = false

var canvas = document.getElementsByTagName('canvas')[0]
canvas.width = 940
canvas.height = 940
var ctx = canvas.getContext('2d')

var currentTool = 'draw'

var closestPointIndex = null
var canMovePoint = false

window.addEventListener("mousemove", () => {
    mousePos = [event.clientX - 3, event.clientY - 3]
    
    if(!canMovePoint){
        checkClosestPoint(currentWall)
    } else {
        movePoint(closestPointIndex, currentWall)
    }

    draw()
})

canvas.addEventListener("mousedown", () => {    
    switch(currentTool){
        case "move":
            if(getDistance(mousePos, currentWall[closestPointIndex]) < 15){
                canMovePoint = true
            }
            break
        case "draw":
            if(shift){
                closeWall()
            } else {
                addPoint(currentWall, currentWallName)
            }
            break
        case "delete":
            if(getDistance(mousePos, currentWall[closestPointIndex]) < 15){
                deletePoint(closestPointIndex)
            }
            break
        case "insert":
            currentWall.splice(closestPointIndex, 0, mousePos)
            break
    }

    draw()
})

window.addEventListener("mouseup", () => {
    canMovePoint = false
})

window.addEventListener("keydown", () => {
    switch(event.keyCode){
        case 16: 
            shift = true
            break
        case 17:
            ctrl = true
            break
    }
    
    // 90 = Z key
    if (ctrl && event.keyCode == 90){
        currentWall.pop()
        draw()
    }
})

window.addEventListener("keyup", () => {
    switch(event.keyCode){
        case 16: 
            shift = false
            break
        case 17:
            ctrl = false
            break
    }
})

document.getElementById('export').onclick = function(){
    var json = {}
    json.innerWall = innerWall
    json.outerWall = outerWall
    
    var data = "text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(json))
    var a = document.createElement('a')
    a.href = 'data:' + data
    a.download = 'track.json'
    a.click()
}

document.getElementById('undo').onclick = function(){
    currentWall.pop()
    draw()
}

document.getElementById('close-wall').onclick = function(){
    closeWall()
}

document.getElementById("outer-wall").onclick = function(){
    currentWall = outerWall
    currentWallName = 'outerWall'
    currentWallClosed = outerWallClosed
}

document.getElementById("inner-wall").onclick = function(){
    currentWall = innerWall
    currentWallName = 'innerWall'
    currentWallClosed = innerWallClosed
}

document.getElementById("draw-tool").onclick = function(){
    currentTool = "draw"
}

document.getElementById("move-tool").onclick = function(){
    currentTool = "move"
}

document.getElementById("delete-tool").onclick = function(){
    currentTool = "delete"
}

document.getElementById("insert-tool").onclick = function(){
    currentTool = "insert"
}

function checkClosestPoint(wall){
    var minDistance = null
    for(var i = 0; i < wall.length; i++){
        var distance = getDistance(mousePos, wall[i])
        if(minDistance == null || distance < minDistance){ 
            minDistance = distance 
            closestPointIndex = i
        }
    }
}

function addPoint(wall){
    if(!currentWallClosed || wall.length < 2){
        wall.push(mousePos)
    }
}

function deletePoint(closestPointIndex){
    currentWall.splice(closestPointIndex, 1)
    draw()
}

function closeWall(){
    if(currentWall.length > 2){
        outerWallClosed = currentWallName == 'outerWall' ? true : false
        innerWallClosed = currentWallName == 'innerWall' ? true : false
        currentWallClosed = currentWallName == 'outerWall' ? outerWallClosed : innerWallClosed
    }
}

function draw(){
    canvas.width = canvas.width

    ctx.fillStyle = 'blue'
    ctx.arc(mousePos[0], mousePos[1], 3, 0, 2 * Math.PI, true)
    ctx.fill()

    drawWall(innerWall, innerWallClosed)
    drawWall(outerWall, innerWallClosed)
    drawPoints(innerWall)
    drawPoints(outerWall)
}

function drawWall(wall, isClosed){
    if(wall.length){
        ctx.beginPath()
        ctx.moveTo(...wall[0])
        for(var i = 1; i < wall.length; i++){
            ctx.lineTo(...wall[i])
        }
        
        if(isClosed){
            ctx.lineTo(...wall[0])
        } else if(currentWall == wall && currentTool == 'draw') {
            ctx.lineTo(...mousePos)
        }
        
        ctx.stroke()
    }
}

function drawPoints(wall){
    ctx.fillStyle = 'blue'
    for(var i = 0; i < wall.length; i++){
        ctx.beginPath()
        ctx.arc(wall[i][0], wall[i][1], 3, 0, 2 * Math.PI, true)
        ctx.fill()
    }

    if(wall.length && currentTool == 'insert'){
        ctx.fillStyle = 'red'
        ctx.beginPath()
        ctx.arc(...wall[closestPointIndex], 3, 0, 2 * Math.PI, true)
        ctx.fill()
    }
}

function getDistance(p1, p2){
    return Math.sqrt(Math.pow(p1[0] - p2[0], 2)+
                     Math.pow(p1[1] - p2[1], 2))
}

function movePoint(index, wall){
    wall[index] = mousePos
    draw()
}