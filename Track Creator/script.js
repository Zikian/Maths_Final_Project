var mousePos = []
var innerWall = []
var outerWall = []
var checkpoints = []

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
var closestPointOnLine = null

var checkpointTargetWall = "outerWall"

var outerWallCheckpoint = null
var innerWallCheckpoint = null

window.addEventListener("mousemove", () => {
    mousePos = [event.clientX - 3, event.clientY - 3]
    
    if(!canMovePoint){
        checkClosestPoint(currentWall)
    } else {
        movePoint(closestPointIndex, currentWall)
    }

    if(currentTool == "checkpoint"){

        if(!outerWallCheckpoint){
            var closestLine = getClosestLine(outerWall)
        } else if (!innerWallCheckpoint){
            var closestLine = getClosestLine(innerWall)
        }

        closestPointOnLine = getClosestPointToLine(closestLine[0], closestLine[1], mousePos)
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
        case "checkpoint":
            if(!outerWallCheckpoint){
                outerWallCheckpoint = closestPointOnLine
            } else if (!innerWallCheckpoint){
                innerWallCheckpoint = closestPointOnLine
            }

            
            if(innerWallCheckpoint && outerWallCheckpoint){
                checkpoints.push([innerWallCheckpoint, outerWallCheckpoint])
                innerWallCheckpoint = null
                outerWallCheckpoint = null
            }
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
    json.checkpoints = checkpoints
    
    var data = "text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(json))
    var a = document.createElement('a')
    a.href = 'data:' + data
    a.download = 'track.json'
    a.click()
}

document.getElementById('import').onclick = function(){
    var input = document.createElement('input')
    input.type = "file"
    input.click()
    input.onchange = function(){
        var reader = new FileReader()

        reader.onload = function(event){
            var jsonObj = JSON.parse(event.target.result);
            innerWall = jsonObj.innerWall
            outerWall = jsonObj.outerWall

            if(JSON.stringify(innerWall[0]) == JSON.stringify(innerWall[innerWall.length - 1])){
                innerWallClosed = true;
            } else {
                innerWallClosed = false;
            }

            if(JSON.stringify(outerWall[0]) == JSON.stringify(outerWall[outerWall.length - 1])){
                outerWallClosed = true;
            } else {
                outerWallClosed = false;
            }

            if(currentWallName == "outerWall"){
                currentWall = outerWall
                currentWallClosed = outerWallClosed
            } else {
                currentWall = innerWall
                currentWallClosed = innerWallClosed
            }

            draw()
        }

        reader.readAsText(event.target.files[0])
    }

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
    checkpointTargetWall = 'outerWall'
}

document.getElementById("inner-wall").onclick = function(){
    currentWall = innerWall
    currentWallName = 'innerWall'
    currentWallClosed = innerWallClosed
    checkpointTargetWall = 'innerWall'
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

document.getElementById("checkpoint-tool").onclick = function(){
    currentTool = "checkpoint"
}

function getClosestLine(wall){
    var minDistanceIndex = null
    var minDistance = null

    for(var i = 0; i < wall.length - 1; i++){
        var p1 = wall[i]
        var p2 = wall[i+1]
        var distance = getDistanceToLine(...mousePos, ...p1, ...p2)
        if(minDistance == null || distance < minDistance){ 
            minDistance = distance 
            minDistanceIndex = i
        }
    }
    var p1 = wall[minDistanceIndex]
    var p2 = wall[minDistanceIndex+1]
    return [p1, p2]
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

    if(currentTool != "checkpoint"){
        ctx.fillStyle = 'blue'
        ctx.arc(mousePos[0], mousePos[1], 3, 0, 2 * Math.PI, true)
        ctx.fill()
    }

    drawWall(innerWall, innerWallClosed)
    drawWall(outerWall, outerWallClosed)
    drawPoints(innerWall)
    drawPoints(outerWall)
    drawCheckpoints()

    if(currentTool == "checkpoint" && closestPointOnLine){
        ctx.fillStyle = 'blue'
        ctx.beginPath()
        ctx.arc(...closestPointOnLine, 3, 0, 2 * Math.PI, true)
        ctx.fill()
    }
}

function drawCheckpoints(){
    ctx.strokeStyle = 'green'

    if(closestPointOnLine){
        if(!innerWallCheckpoint && outerWallCheckpoint){
            ctx.beginPath()
            ctx.moveTo(...outerWallCheckpoint)
            ctx.lineTo(...closestPointOnLine)
            ctx.stroke()
        } 
        
        if (innerWallCheckpoint !=null && outerWallCheckpoint == null){
            ctx.beginPath()
            ctx.moveTo(...innerWallCheckpoint)
            ctx.lineTo(...closestPointOnLine)
            ctx.stroke()
        }
    }

    for(var i = 0; i < checkpoints.length; i++){
        ctx.beginPath()
        ctx.moveTo(...checkpoints[i][0])
        ctx.lineTo(...checkpoints[i][1])
        ctx.stroke()
    }
}

function drawWall(wall, isClosed){
    ctx.strokeStyle = 'black'
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

function getClosestPointToLine(p1, p2, p){
    var a = (p2[1] - p1[1]) / (p2[0] - p1[0]) 
    var c = a * -p1[0] + p1[1]
    var b = -1/a
    var d = b * -p[0] + p[1]
    
    x = (d-c)/(a-b)
    y = a*x + c

    if(!pointOnLineSegment(p1, p2, [x,y])){
        return null
    }

    return [x, y]
}

function pointOnLineSegment(p1, p2, p){
    var dot = (p[0] - p1[0]) * (p2[0] - p1[0]) + (p[1] - p1[1])*(p2[1] - p1[1])
    if (dot < 0){
        return false
    }
    
    var squaredlength = Math.pow(p2[0] - p1[0], 2) + Math.pow(p2[1] - p1[1], 2)
    if (dot > squaredlength){
        return false
    }

    return true
}

function getDistanceToLine(x, y, x1, y1, x2, y2) {
    var A = x - x1;
    var B = y - y1;
    var C = x2 - x1;
    var D = y2 - y1;
  
    var dot = A * C + B * D;
    var len_sq = C * C + D * D;
    var param = -1;
    if (len_sq != 0) //in case of 0 length line
        param = dot / len_sq;
  
    var xx, yy;
  
    if (param < 0) {
      xx = x1;
      yy = y1;
    }
    else if (param > 1) {
      xx = x2;
      yy = y2;
    }
    else {
      xx = x1 + param * C;
      yy = y1 + param * D;
    }
  
    var dx = x - xx;
    var dy = y - yy;
    return Math.sqrt(dx * dx + dy * dy);
}

function movePoint(index, wall){
    wall[index] = mousePos
    draw()
}