# version 330 core

in vec2 v_uv;
out vec4 fragColor;
uniform vec2 a_resolution;
uniform float a_time;
uniform vec2 a_mouse;

vec2 iResolution = a_resolution;
vec2 fragCoord = v_uv*iResolution;
float iTime = a_time;
vec2 iMouse = a_mouse;


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
float smax(in float a,in float b,in float k)
{
	float h = max(k-abs(a-b),0.0);
    return max(a,b) + h*h/(k*4.0);

}

vec2 sdGuy(vec3 pos)
{
    float t = fract(iTime);
    //t = 0.5;
    float y = 4.0*t*(1.0-t);
    vec3 cen = vec3(0.0,y,0.0);
    float sy = 0.5+0.5*y;
    float sz = 1.0/sy;
    vec3 rad = vec3(0.25,0.25*sy,0.25*sz);	//radius
    vec3 pos_body = pos-cen;	
    float d_body = sdElipsoid(pos_body,rad);
    vec3 sh = vec3(abs(pos_body.x),pos_body.yz);
    //head
    float d_head = sdElipsoid(pos_body-vec3(0.0,0.28,0.0),vec3(0.15,0.2,0.23));
    float d = smin(d_body,d_head,0.1);
    float d_back_head = sdElipsoid(pos_body-vec3(0.0,0.28,-0.1),vec3(0.2,0.2,0.2));
	d = smin(d,d_back_head,0.03);
    vec3 eb = sh-vec3(0.12,0.34,0.15);
    eb.xy = mat2(3,4,-4,3)/5.0*eb.xy;
    float d_eye_brows = sdElipsoid(eb,vec3(0.06,0.035,0.05));
    d = smin(d_eye_brows,d,0.04);
    
    //mouth
    float d_mouth = sdElipsoid(pos_body-vec3(0.0,0.15+3.0*pos_body.x*pos_body.x,0.1),vec3(0.1,0.04,0.15));
    d = smax(d,-d_mouth,0.04);
    vec2 res = vec2(d,2.0); 
    //eyes
    float d_eyes = sdSphere(sh - vec3(0.08,0.28,0.16),0.05);
    if(d_eyes<d)
    {
    	res = vec2(d_eyes,3.0);
    }
    float d_pupils = sdSphere(sh - vec3(0.08,0.28,0.18),0.02);
    if(d_pupils<d)
    {
    	res = vec2(d_pupils,4.0);
    }
    
    return res;
}
vec2 map(in vec3 pos)
{
    vec2 d1 = sdGuy(pos);
    float d2 = pos.y-(-0.25);
    return (d2<d1.x)?vec2(d2,1.0):d1;
}
float castShadow(in vec3 ro,in vec3 rd)
{
    float res = 1.0;
    float t = 0.001;
    for(int i=0;i<100;i++)
    {
        vec3 pos = ro + rd*t;
        float h = map(pos).x;
        res = min(res,16.0*h/t);
        t+=h;
        if(t>20.0)
            break;
    }
    return res;
}

vec3 calcNormal(in vec3 pos)
{
    vec2 e = vec2(0.00001,0.0);
    return normalize(vec3(
        			map(pos+e.xyy).x-map(pos-e.xyy).x,
        			map(pos+e.yxy).x-map(pos-e.yxy).x,
			        map(pos+e.yyx).x-map(pos-e.yyx).x) );
        
}
vec2 castRay(in vec3 ro ,in vec3 rd)
{
	float obj=-1.0;
    float t = 0.0;
    for(int i=0;i<100;i++)
    {
        vec3 pos = ro + t*rd;
        vec2 h = map(pos);
        obj = h.y;
        if(h.x<0.001)
            break;
        t = t+h.x;
        if(t>20.0) {
        	obj=-1.0;
            break;
        }
    }
    if(t>20.0)
        t=-1.0;
    return vec2(t,obj);
}

void main()
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
    vec2 t_obj = castRay(ro,rd);
    if(t_obj.y>0.0)
    {
    	float t = t_obj.x;
        vec3 pos = ro+t*rd;
        vec3 nor = calcNormal(pos);
        vec3 mate = vec3(0.18);
        if(t_obj.y<1.5)
        {
        	mate = vec3(0.05,0.1,0.02);
        }
        else if(t_obj.y<2.5)
        {
        	mate = vec3(0.2,0.1,0.02);
        }
        else if(t_obj.y<3.5)
        {
        	mate = vec3(0.4,0.4,0.4);
        }
        else if(t_obj.t<4.5)
        {
        	mate = vec3(0.01);
        }
        vec3 sun_dir = normalize(vec3(0.8,0.3,0.2));
        float sun_dif = clamp(dot(sun_dir,nor),0.0,1.0);
        float sun_sha = castShadow(pos+nor*0.001,sun_dir);
        float sky_dif = clamp(0.5+0.5*dot(nor,vec3(0.0,1.0,0.0)),0.0,1.0);
        float bou_dif = clamp(0.5+0.5*dot(nor,vec3(0.0,-1.0,0.0)),0.0,1.0);
        //sun_sha = 1.0;
        col = mate*vec3(7.0,5.0,3.0)*sun_dif*sun_sha;
        col += mate*vec3(0.5,0.8,0.9)*sky_dif;
        col += mate*vec3(0.7,0.3,0.2)*bou_dif;
    }
    col = pow(col,vec3(0.4545));
    // Output to screen
    fragColor = vec4(col,1.0);
        
        
}