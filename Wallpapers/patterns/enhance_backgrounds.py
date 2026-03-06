#!/usr/bin/env python3
import re
import os

# File configurations with color themes
file_configs = {
    "11-cosmic-purple.html": {
        "bg_colors": ["#2c3e50", "#1a1a2e", "#0a0a1a"],
        "accent": "#e74c3c",
        "particle_colors": ["#e74c3c", "#c0392b", "#ff6b6b"],
        "type": "cosmic",
    },
    "12-ocean-teal.html": {
        "bg_colors": ["#ff6600", "#cc5200", "#4a1a00"],
        "accent": "#ff6600",
        "particle_colors": ["#ff6600", "#ff8533", "#ffb380"],
        "type": "embers",
    },
    "13-sunset-amber.html": {
        "bg_colors": ["#ffcc00", "#ff9900", "#663300"],
        "accent": "#ffcc00",
        "particle_colors": ["#ffcc00", "#ffe066", "#fff5cc"],
        "type": "amber",
    },
    "14-forest-green.html": {
        "bg_colors": ["#2ecc71", "#27ae60", "#0a2a1a"],
        "accent": "#2ecc71",
        "particle_colors": ["#2ecc71", "#58d68d", "#82e0aa"],
        "type": "forest",
    },
    "15-neon-pink.html": {
        "bg_colors": ["#ff69b4", "#ff1493", "#1a000d"],
        "accent": "#ff69b4",
        "particle_colors": ["#ff69b4", "#ff1493", "#ff85c2"],
        "type": "neon",
    },
    "16-arctic-blue.html": {
        "bg_colors": ["#5dade2", "#3498db", "#0a1f2e"],
        "accent": "#5dade2",
        "particle_colors": ["#5dade2", "#85c1e9", "#aed6f1"],
        "type": "arctic",
    },
    "17-rose-red.html": {
        "bg_colors": ["#e79e8e", "#c0392b", "#2a0a05"],
        "accent": "#e79e8e",
        "particle_colors": ["#e79e8e", "#f5b7b1", "#fadbd8"],
        "type": "rose",
    },
    "18-emerald-teal.html": {
        "bg_colors": ["#48c9b0", "#1abc9c", "#0a2a25"],
        "accent": "#48c9b0",
        "particle_colors": ["#48c9b0", "#76d7c4", "#a3e4d7"],
        "type": "emerald",
    },
    "19-golden-yellow.html": {
        "bg_colors": ["#f7dc6f", "#f1c40f", "#2a2200"],
        "accent": "#f7dc6f",
        "particle_colors": ["#f7dc6f", "#f9e79f", "#fcf3cf"],
        "type": "golden",
    },
    "20-lavender-indigo.html": {
        "bg_colors": ["#bb8fce", "#9b59b6", "#1a0a25"],
        "accent": "#bb8fce",
        "particle_colors": ["#bb8fce", "#d2b4de", "#e8daef"],
        "type": "lavender",
    },
    "21-autumn-orange.html": {
        "bg_colors": ["#f0b27a", "#e67e22", "#2a1500"],
        "accent": "#f0b27a",
        "particle_colors": ["#f0b27a", "#f5cba7", "#fdebd0"],
        "type": "autumn",
    },
    "22-tropical-cyan.html": {
        "bg_colors": ["#4dd0e1", "#00bcd4", "#001a1f"],
        "accent": "#4dd0e1",
        "particle_colors": ["#4dd0e1", "#80deea", "#b2ebf2"],
        "type": "tropical",
    },
    "23-magenta-dream.html": {
        "bg_colors": ["#c39bd3", "#8e44ad", "#1a0a1f"],
        "accent": "#c39bd3",
        "particle_colors": ["#c39bd3", "#d7bde2", "#ebdef0"],
        "type": "magenta",
    },
    "24-lime-forest.html": {
        "bg_colors": ["#a569bd", "#7d3c98", "#0a140a"],
        "accent": "#a569bd",
        "particle_colors": ["#a569bd", "#bb8fce", "#d2b4de"],
        "type": "purple_green",
    },
    "25-mustard-field.html": {
        "bg_colors": ["#52be80", "#27ae60", "#0a140a"],
        "accent": "#52be80",
        "particle_colors": ["#52be80", "#7dcea0", "#a9dfbf"],
        "type": "green_field",
    },
    "26-royal-purple.html": {
        "bg_colors": ["#f7dc6f", "#f39c12", "#1a0a28"],
        "accent": "#f7dc6f",
        "particle_colors": ["#f7dc6f", "#f9e79f", "#fcf3cf"],
        "type": "royal",
    },
    "27-coral-red.html": {
        "bg_colors": ["#bb8fce", "#9b59b6", "#140a0a"],
        "accent": "#bb8fce",
        "particle_colors": ["#bb8fce", "#d2b4de", "#e8daef"],
        "type": "coral",
    },
    "28-sky-blue.html": {
        "bg_colors": ["#f1948a", "#e74c3c", "#0a1420"],
        "accent": "#f1948a",
        "particle_colors": ["#f1948a", "#f5b7b1", "#fadbd8"],
        "type": "coral_blue",
    },
    "29-spring-green.html": {
        "bg_colors": ["#85c1e9", "#3498db", "#1a0a0a"],
        "accent": "#85c1e9",
        "particle_colors": ["#85c1e9", "#aed6f1", "#d6eaf8"],
        "type": "spring_blue",
    },
    "30-mystic-violet.html": {
        "bg_colors": ["#82e0aa", "#2ecc71", "#0a140a"],
        "accent": "#82e0aa",
        "particle_colors": ["#82e0aa", "#abebc6", "#d5f4e6"],
        "type": "mystic_green",
    },
}


def generate_enhanced_bg(filename, config):
    colors = config["particle_colors"]
    accent = config["accent"]

    # Generate particle array setup
    particle_setup = f"""const particles=[],waves=[],glows=[],floaters=[];
    for(let i=0;i<60;i++)particles.push({{x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-0.5)*0.5,vy:(Math.random()-0.5)*0.5,s:1+Math.random()*2,a:Math.random()*0.5+0.2,phase:Math.random()*Math.PI*2}});
    for(let i=0;i<5;i++)waves.push({{y:H*0.4+i*H*0.12,amp:15+i*8,freq:0.008+i*0.003,speed:0.001+i*0.0002,phase:i,color:['{colors[0]}','{colors[1]}','{colors[2]}'][i%3]}});
    for(let i=0;i<8;i++)glows.push({{x:Math.random()*W,y:Math.random()*H,r:50+Math.random()*80,vx:(Math.random()-0.5)*0.3,vy:(Math.random()-0.5)*0.3,phase:Math.random()*Math.PI*2,color:'{colors[i % len(colors)]}'}});
    for(let i=0;i<40;i++)floaters.push({{x:Math.random()*W,y:Math.random()*H,vy:0.2+Math.random()*0.4,vx:(Math.random()-0.5)*0.3,s:2+Math.random()*3,a:Math.random()*0.4+0.2,phase:Math.random()*Math.PI*2}});"""

    # Generate enhanced db function
    db_function = f"""function db(t){{
        // Animated multi-layer gradient background
        const cx=W/2+Math.sin(t*0.0005)*80,cy=H/2+Math.cos(t*0.0007)*60;
        const g=x.createRadialGradient(cx,cy,0,W/2,H/2,Math.max(W,H));
        g.addColorStop(0,'{config["bg_colors"][0]}');g.addColorStop(0.4,'{config["bg_colors"][1]}');g.addColorStop(0.8,'{config["bg_colors"][2]}');g.addColorStop(1,'#000');
        x.fillStyle=g;x.fillRect(0,0,W,H);
        // Pulsing glow orbs
        for(let gl of glows){{gl.x+=gl.vx;gl.y+=gl.vy;if(gl.x<-gl.r)gl.x=W+gl.r;if(gl.x>W+gl.r)gl.x=-gl.r;if(gl.y<-gl.r)gl.y=H+gl.r;if(gl.y>H+gl.r)gl.y=-gl.r;const pulse=0.25+Math.sin(t*0.002+gl.phase)*0.15;const gg=x.createRadialGradient(gl.x,gl.y,0,gl.x,gl.y,gl.r);gg.addColorStop(0,gl.color+Math.floor(pulse*255).toString(16).padStart(2,'0'));gg.addColorStop(1,'transparent');x.fillStyle=gg;x.globalAlpha=pulse;x.beginPath();x.arc(gl.x,gl.y,gl.r,0,Math.PI*2);x.fill();}}
        // Animated wave patterns
        x.globalAlpha=0.2;
        for(let w of waves){{x.strokeStyle=w.color;x.lineWidth=2;x.beginPath();for(let wx=0;wx<=W;wx+=15){{const wy=w.y+Math.sin(wx*w.freq+t*w.speed*1000+w.phase)*w.amp*Math.sin(t*0.0005);wx===0?x.moveTo(wx,wy):x.lineTo(wx,wy);}}x.stroke();}}
        // Floating particles
        x.globalAlpha=1;
        for(let p of particles){{p.x+=p.vx;p.y+=p.vy;if(p.x<0)p.x=W;if(p.x>W)p.x=0;if(p.y<0)p.y=H;if(p.y>H)p.y=0;const pulse=0.6+Math.sin(t*0.003+p.phase)*0.4;x.globalAlpha=p.a*pulse;x.fillStyle='{colors[0]}';x.beginPath();x.arc(p.x,p.y,p.s,0,Math.PI*2);x.fill();}}
        // Rising/flowing elements
        for(let f of floaters){{f.y+=f.vy;f.x+=f.vx+Math.sin(t*0.001+f.phase)*0.5;if(f.y>H)f.y=0;if(f.x<0)f.x=W;if(f.x>W)f.x=0;x.globalAlpha=f.a;x.fillStyle='{colors[1]}';x.beginPath();x.arc(f.x,f.y,f.s*(0.8+Math.sin(t*0.004+f.phase)*0.2),0,Math.PI*2);x.fill();}}
        // Final color overlay
        x.globalAlpha=0.1;const mg=x.createLinearGradient(0,0,W,H);mg.addColorStop(0,'{accent}40');mg.addColorStop(1,'transparent');x.fillStyle=mg;x.fillRect(0,0,W,H);x.globalAlpha=1;
    }}"""

    return particle_setup, db_function


# Process each file
for filename, config in file_configs.items():
    filepath = os.path.join(
        "/Users/lucky/Desktop/Projects/HTMLWall/Wallpapers/patterns", filename
    )
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            content = f.read()

        # Find and replace the db function
        # This is a simple replacement - the full implementation would need careful parsing
        print(f"Processing {filename}...")
    else:
        print(f"File not found: {filename}")
