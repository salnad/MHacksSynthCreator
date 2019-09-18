const express = require('express')
//const test = require('./test.js')
const app = express()

global.dataArray = runPython()

function runPython(){
	const spawn = require("child_process").spawn;
	const pythonProcess = spawn('python', ["yo2.py"])
	pythonProcess.stdout.on('data', (data) => {
		dataArray = prettify(data)
		dataArray = normalize(dataArray)
		//console.log(dataArray)
		return dataArray;
		global.dataArray = data
		console.log(data)
	});
}

app.get('/data', function(req, res) {
	if(typeof dataArray !== 'undefined'){
		res.setHeader("Access-Control-Allow-Origin", "*");
		res.setHeader("Content-Type", "text/plain")
	    console.log(dataArray[0] + "-" + dataArray[1])
	    //res.setHeader('Content-Type', 'text/plain')
	    // res.setHeader('Access-Control-Allow-Origin', '*')
	    res.send(dataArray[0] + "-" + dataArray[1])
		//res.sendFile("./index.html", {root: __dirname});
	}

	console.log(global.dataArray)
});

app.get('/populate', function(req, res){
	//global.dataArray = runPython()
});

function prettify(data) {
	data = data.toString('utf8');
	dataArr = data.split("-");

	dataArr[1] = dataArr[1].substring(0, dataArr[1].length-2)
	//console.log(dataArr)
	return dataArr
}

function normalize(dataArray){
	dataArray[0] = (300-dataArray[0])/300
	dataArray[1] = (300-dataArray[1])/300

	if(dataArray[0] == 1 && dataArray[1] == 1){
		dataArray[0] = 0;
		dataArray[1] = 0;
	}

	return dataArray
}

function getPointArray(){
	return this.dataArray
}
app.listen(8000)