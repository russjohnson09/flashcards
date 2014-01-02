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
    "r" : 10,
    "bullet_spawn" : 10,
    "last_spawn" : 0
};

var bulletpros = [];
var pbullets = [];

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
    "spawnrate" : 20,
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
    "upperlim" : 300,
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


function handle_player() {
    var b;
    
    for (var i = bullets.length-1; i > -1; i--) {
        b = bullets[i];
        if (collision(p,b)) {
            p.lives--;
            bullets.splice(i,1);
        }
    }
    
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
    
    if (z) {
        if (p.bullet_spawn < (frame - p.last_spawn)){
            var pbullet = {"x":p.x,
                           "y":p.y,
                           "vx":0,
                           "vy":-10,
                           "r":2};
            pbullets[pbullets.length] = pbullet;
            p.last_spawn = frame;
        }
    }
    
    c.fillStyle="#FF0000";
    c.beginPath();
    c.arc(p.x,p.y,p.r,0,2*Math.PI);
    c.fill();
}

function handle_pbullets() {
    var b;
    for (var i = pbullets.length-1; i > -1; i--)
	{
        b = pbullets[i];
        b.x += b.vx;
        b.y += b.vy;
        if (out(b)){
            pbullets.splice(i,1);
            return;
        }
        c.beginPath();
        c.arc(b.x,b.y,b.r,0,2*Math.PI);
        c.fill();
	}
}

function handle_enemies(){
    var e;
    var b;
    var bulletpro;
	for (var i = enemies.length -1; i > -1; i--)
	{
        e = enemies[i];
        if (out(e)){
            enemies.splice(i,1);
            return;
        }
        e.vx += e.ax;
        e.vy += e.ay;
        e.x += e.vx;
        e.y += e.vy;
		
        for (var j = pbullets.length-1; j > -1; j--) {
            if (collision(e,pbullets[j])){
                e.health--;
                pbullets.splice(j,1);
            }
        }
        
		if (e.health < 0)
			enemies.splice(i, 1);
        else {
            c.fillStyle="#FF0000";
            c.beginPath();
            c.arc(e.x,e.y,e.r,0,2*Math.PI);
            c.fill();
            
            bulletpro = e.bulletprofile;
            if (((frame - e.spawned) - bulletpro.last_spawn) > bulletpro.spawnrate) {
                b = $.extend({},bulletpro.bullet);
                b.x += e.x;
                b.y += e.y;
                bullets[bullets.length]=b;
                bulletpro.last_spawn = frame;
            }
        }
	}
}

function handle_bullets() {
    var b;
    for (var i = bullets.length - 1; i > -1; i--)
	{
        b = bullets[i];
        b.x += b.vx;
        b.y += b.vy;
        
        if (out(b)){
            bullets.splice(i,1);
            return;
        }
        c.beginPath();
        c.arc(b.x,b.y,b.r,0,2*Math.PI);
        c.fill();
	}
}

function spawn() {
    var enemypro;
    for (var i=enemypros.length-1; i > -1; i--) {
        enemypro=enemypros[i];
        if (enemypro.upperlim < frame) {
            enemypros.splice(i, 1);
        }
        else if ( frame > enemypro.lowerlim && (frame - enemypro.last_spawn) > enemypro.spawnrate) {
            enemies[enemies.length]=$.extend(true,{},enemypro.enemy);
            enemypro.last_spawn=frame;
        }
    }
}


function loop() {
    frame += 1;
    c.fillStyle = b;
    c.fillRect(0, 0, WIDTH, HEIGHT);
    
    handle_player();
    spawn();
    
    handle_pbullets();
    handle_enemies();
	handle_bullets();
}

function out(o) {
    return ((o.x + o.r < -10) || (o.y + o.r < -10) || (o.x > WIDTH + o.r + 10) || (o.y > HEIGHT + o.r + 10));
}

function collision(o1, o2) {
    return Math.pow((o1.x - o2.x),2) + Math.pow((o1.y - o2.y),2) < Math.pow(o1.r + o2.r,2);
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



function init() {
    var cnv = document.getElementById('c');
    c = cnv.getContext('2d');
}

function level1() {
    var epro;
    enemypros[0] = $.extend(true,{},standardEnemyPro);
    epro = $.extend(true,{},standardEnemyPro);
    epro.lowerlim = 100;
    epro.spawnrate = 11;
    enemypros[1] = epro;
    
    epro = $.extend(true,{},standardEnemyPro);
    epro.lowerlim = 300;
    epro.spawnrate = 10;
    epro.vy = 10;
    epro.ay = -1;
    epro.enemy.bulletprofile.bullet.vx = 1;
    epro.enemy.bulletprofile.spawnrate = 5;
    enemypros[2] = epro;
}

$(function () {
    init();
    level1();
    interval = setInterval(loop, 20); 
});