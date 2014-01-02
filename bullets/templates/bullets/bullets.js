/*global $, jQuery*/


var c;
var b = 'rgb(0,0,0)';
var w = 'rgb(255,255,255)';
var frame = 0;
var WIDTH = 500;
var HEIGHT = 550;
var p = {
    "lives" : 100,
    "speed" : 10,
    "x" : 240,
    "y" : 440,
    "r" : 10
};

var bulletpros = [];

var standardBullet = {
    "health" : 999999,
    "x" : 0,
    "y" : 0,
    "vx" : 0,
    "vy" : 1,
    "ax" : 0,
    "ay" : 0,
    "r" : 2
};

var standardBulletPro = {
    "bullet" : standardBullet,
    "spawnrate" : 10,
    "last_spawn" : 0
};

var enemypros = [];

var standardEnemey = {
    "health" : 1,
    "x" : -1,
    "y" : 10,
    "vx" : 2,
    "vy" : 0,
    "ax" : 0,
    "ay" : 0,
    "r" : 10,
    "bulletprofile" : standardBulletPro,
    "spawned" : 0
};

var standardEnemyPro = {
    "enemy" : standardEnemey,
    "spawnrate" : 20,
    "lowerlim" : 0,
    "upperlim" : 99999999,
    "last_spawn" : 0
};


// sprite arrays
var bullets = [];
var enemies = [];

// which buttons have been pressed
var u = 0; //movement up,down,left,right
var d = 0;
var l = 0;
var r = 0; 
var z = 0; //shoot
var interval;

$(function () {
    init();
    level1();
    interval = setInterval(loop, 20); 
});

function loop()
{
    frame += 1;
    c.fillStyle = b;
    c.fillRect(0, 0, WIDTH, HEIGHT);
    
    handle_player();
    spawn();
    
    c.fillStyle="#FF0000";
    c.beginPath();
    c.arc(p.x,p.y,p.r,0,2*Math.PI);
    c.fill();
    
	// handle enemies
	for (var i = 0; i < enemies.length; i++)
	{
        var e = enemies[i];
        handle_enemy(e);
		
		if (e.dead)
			enemies.splice(i, 1);
        else {
            c.beginPath();
            c.arc(e.x,e.y,e.r,0,2*Math.PI);
            c.fill();
        }
	}
	
	// handle bullets
	for (var i = 0; i < bullets.length; i++)
	{
        var bullet = bullets[i];
        handle_bullet(bullet);
        
		if (bullet.dead == 1)
			bullets.splice(i, 1);
        else {
            c.beginPath();
            c.arc(bullet.x,bullet.y,bullet.r,0,2*Math.PI);
            c.fill();
        }
            
	}
    //draw();
    //print();
}

function draw() {
    
}

//update any stats
function print() {
    
}

// check if objects
function area_overlap(o1,o2)
{
    
	return ((area2.x2 < area2.x1 || area2.x2 > area1.x1) &&
	        (area2.y2 < area2.y1 || area2.y2 > area1.y1) &&
	        (area1.x2 < area1.x1 || area1.x2 > area2.x1) &&
	        (area1.y2 < area1.y1 || area1.y2 > area2.y1));
}

// generate random number between sn and en
function rand(sn, en)
{
	return rn = Math.floor(Math.random()*(en-sn+1))+sn;
}

$( "body" ).keydown(function(e) {
    var keycode = e.which
	if (keycode == 37) l = 1;		// left
	else if (keycode == 38) u = 1;	// up
	else if (keycode == 39) r = 1;	// right
	else if (keycode== 40) d = 1;	// down
	else if (keycode == 90) z = 1;	// z: shot
});

$( "body" ).keyup(function(e) {
    var keycode = e.which
	if (keycode == 37) l = 0;		// left
	else if (keycode == 38) u = 0;	// up
	else if (keycode == 39) r = 0;	// right
	else if (keycode== 40) d = 0;	// down
	else if (keycode == 90) z = 0;	// z: shot
});

function handle_player() {
    var s = p.speed
    p.x += (r-l) * s;
    p.y += (d-u) * s;
    if ((p.x + p.r) > WIDTH) {
        p.x = WIDTH - p.r;
    }
    else if (p.x < p.r) {
        p.x = p.r;
    }
    
    if ((p.y + p.r) > HEIGHT) {
        p.y = HEIGHT - p.r;
    }
    else if (p.y < p.r) {
        p.y = p.r;
    }
}

function handle_enemy(e) {
    e.vx += e.ax;
    e.vy += e.ay;
    e.x += e.vx;
    e.y += e.vy;
    
    var bulletpro = e.bulletprofile;
    
    if (((frame - e.spawned) - bulletpro.last_spawn) > bulletpro.spawnrate) {
        var b1 = bulletpro.bullet;
        var b2 = {
            "health" : b1.health,
            "x" : e.x + b1.x,
            "y" : e.y + b1.y,
            "vx" : b1.vx,
            "vy" : b1.vy,
            "ax" : b1.ax,
            "ay" : b1.ay,
            "r" : b1.r
            };
        bullets[bullets.length]=b2
    }
}

function handle_bullet(b) {
    b.vx += b.ax;
    b.vy += b.ay;
    b.x += b.vx;
    b.y += b.vy;
}

function spawn(enemypro) {
    var enemypro;
    for (var i = 0; i < enemypros.length; i++) {
        enemypro=enemypros[i];
        if (enemypro.upperlim < frame) {
            enemypros.splice(i, 1);
        }
        else if ( frame > enemypro.lowerlim && (frame - enemypro.last_spawn) > enemypro.spawnrate) {
            var e1 = enemypro.enemy;
            var e2 = {
                "health" : e1.health,
                "x" : e1.x,
                "y" : e1.y,
                "vx" : e1.vx,
                "vy" : e1.vy,
                "ax" : e1.ax,
                "ay" : e1.ay,
                "r" : e1.r,
                "bulletprofile" : e1.bulletprofile,
                "spawned" : frame
                };
            enemies[enemies.length]=e2;
            enemypro.last_spawn=frame;
        }
    }
}


function init() {
    var cnv = document.getElementById('c');
    c = cnv.getContext('2d');
}

function level1() {
    enemypros[0] = standardEnemyPro;
}