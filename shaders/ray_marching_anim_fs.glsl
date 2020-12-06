float map(in vec3 pos)
{
    float d = length(pos)-0.25;
    float d2 = pos.y-(-0.25);
    return min(d,d2);
    
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
	vec3 ro = vec3(0.0,0.0,1.0);	//ray origion(camera)
    vec3 rd = normalize(vec3(p,-1.5));
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