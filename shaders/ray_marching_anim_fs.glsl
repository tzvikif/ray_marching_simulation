float sdElipsoid(in vec3 pos,in vec3 rad)
{
    float k0 = length(pos/rad);
    float k1 = length(pos/rad/rad);
    return k0*(k0-1.0)/k1;
}
float sdSphere(in vec3 pos,in float rad)
{
	float d = length(pos) - rad;
    return d;
}
float smin(in float a,in float b,in float k)
{
	float h = max(k-abs(a-b),0.0);
    return min(a,b) - h*h/(k*4.0);

}
float sdGuy(vec3 pos)
{
    float t = fract(iTime);
    //t = 0.5;
    float y = 4.0*t*(1.0-t);
    vec3 cen = vec3(0.0,y,0.0);
    float sy = 0.5+0.5*y;
    float sz = 1.0/sy;
    vec3 rad = vec3(0.25,0.25*sy,0.25*sz);
    vec3 q = pos-cen;
    float d_body = sdElipsoid(q,rad);
    //head
    vec3 pos_head = vec3(q) - vec3(0.0,0.28,0.0);
    float d_head = sdElipsoid(pos_head,vec3(0.2));
    float d_back_head = sdElipsoid(pos_head+vec3(0.0,0.0,0.1),vec3(0.2));
	float d = smin(d_head,d_back_head,0.03);
    d = smin(d_body,d,0.1);
    //eyes
    float d_eyes = sdSphere(pos_head - vec3(0.15,0.15,-0.15),0.05);
    
    return min(d,d_eyes);
}
float map(in vec3 pos)
{
    float d1 = sdGuy(pos);
    float d2 = pos.y-(-0.25);
    return min(d1,d2);
    
}
vec3 calcNormal(in vec3 pos)
{
    vec2 e = vec2(0.00001,0.0);
    return normalize(vec3(
        			map(pos+e.xyy)-map(pos-e.xyy),
        			map(pos+e.yxy)-map(pos-e.yxy),
			        map(pos+e.yyx)-map(pos-e.yyx)) );
        
}
float castRay(in vec3 ro ,in vec3 rd)
{
    float t = 0.0;
    for(int i=0;i<100;i++)
    {
        vec3 pos = ro + t*rd;
        float h = map(pos);
        if(h<0.001)
            break;
        t = t+h;
        if(t>20.0)
            break;
    }
    if(t>20.0)
        t=-1.0;
    return t;
}

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    // Normalized pixel coordinates (from 0 to 1)
    vec2 p = (2.0*fragCoord-iResolution.xy)/iResolution.y;
    float an = 10.0*iMouse.x/iResolution.x;// iTime;
    vec3 ta = vec3(0.0,0.8,0.0);
    vec3 ro = ta+vec3(1.5*sin(an),0.0,1.5*cos(an));	//ray origion(camera)
    
    vec3 ww = normalize(ta-ro);
    vec3 uu = normalize(cross(ww,vec3(0.0,1.0,0.0)) );
    vec3 vv = normalize( cross(uu,ww) );
    
    
    vec3 rd = normalize(p.x*uu+p.y*vv+1.8*ww);
    vec3 col = vec3(0.4,0.75,1.0) - 0.5*p.y;
    col = mix(col,vec3(0.7,0.75,0.8),exp(-10.0*rd.y));
    float t = castRay(ro,rd);
    if(t>0.0)
    {
        vec3 pos = ro+t*rd;
        vec3 nor = calcNormal(pos);
        vec3 mate = vec3(0.18);
        vec3 sun_dir = normalize(vec3(0.8,0.3,0.2));
        float sun_dif = clamp(dot(sun_dir,nor),0.0,1.0);
        float sun_sha = step(castRay(pos+nor*0.001,sun_dir),0.0);
        float sky_dif = clamp(0.5+0.5*dot(nor,vec3(0.0,1.0,0.0)),0.0,1.0);
        float bou_dif = clamp(0.5+0.5*dot(nor,vec3(0.0,-1.0,0.0)),0.0,1.0);
        //sun_sha = 0.0;
        col = mate*vec3(7.0,5.0,3.0)*sun_dif*sun_sha;
        col += mate*vec3(0.5,0.8,0.9)*sky_dif;
        col += mate*vec3(0.7,0.3,0.2)*bou_dif;
    }
    col = pow(col,vec3(0.4545));
    // Output to screen
    fragColor = vec4(col,1.0);
        
        
}