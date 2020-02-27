// frame timing function
(function () {
	var requestAnimationFrame = window.requestAnimationFrame || window.msRequestAnimationFrame || window.mozRequestAnimationFrame || window.webkitRequestAnimationFrame;
	window.requestAnimationFrame = requestAnimationFrame;
})();

// define canvas and its context
var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");

// canvas properties
canvas.width = window.innerWidth * 0.85;
canvas.height = window.innerHeight * 0.9;

// mobile settings
var deviceMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)

// game settings
var fps = 60;
var friction = 0.95;
var pause = true;
var crush = false;
var uncrush = false;

// mouse
var mouse = {
	x: 0,
	y: 0,
	onCanvas: false,
	cursor: "default"
};

// get mouse position for desktop
function mousePositionDesktop(e) {
	if (!deviceMobile) {
		mouse.x = e.x - canvas.getBoundingClientRect().left;
		mouse.y = e.y - canvas.getBoundingClientRect().top;
	}
}

canvas.addEventListener("mousemove", mousePositionDesktop);

// toggle mouse.onCanvas and other variables for whether the mouse is on canvas
function mouseEnter() {
	mouse.onCanvas = true;
	pause = false;
}

function mouseLeave() {
	mouse.onCanvas = false;
}

canvas.addEventListener("mouseenter", mouseEnter);
canvas.addEventListener("mouseleave", mouseLeave);

// get mouse position for mobile
function mousePositionMobile(e) {
	// setting mouse coordinates
	var x = e.touches[0].clientX - canvas.getBoundingClientRect().left;
	var y = e.touches[0].clientY - canvas.getBoundingClientRect().top;

	return {
		x: x,
		y: y
	};
}

// update game
function tick() {
	render();

	// recalls tick at appropriate fps
	setTimeout(function() {
		requestAnimationFrame(tick)
	}, 1000/fps);
}

// render
function render() {
	// background
	ctx.fillStyle = "#0062ff";
	ctx.fillRect(0, 0, canvas.width, canvas.height);
}

window.onload = function() {
	tick();
	render();
}