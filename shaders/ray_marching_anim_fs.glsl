float map(in vec3 pos)
{
    float d = length(pos)-0.25;
    return d;
    
}
vec3 calcNormal(in vec3 pos)
{
    vec2 e = vec2(0.00001,0.0);
    return normalize(vec3(
        			map(pos+e.xyy)-map(pos-e.xyy),
        			map(pos+e.yxy)-map(pos-e.yxy),
			        map(pos+e.yyx)-map(pos-e.yyx)) );
        
}

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    // Normalized pixel coordinates (from 0 to 1)
    vec2 p = (2.0*fragCoord-iResolution.xy)/iResolution.y;
	vec3 ro = vec3(0.0,0.0,1.0);	//ray origion(camera)
    vec3 rd = normalize(vec3(p,-1.5));
    vec3 col = vec3(0.0);
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
    if(t<20.0)
    {
        vec3 pos = ro+t*rd;
        vec3 nor = calcNormal(pos);
        col = nor.yyy;
    }
    // Output to screen
    fragColor = vec4(col,1.0);
        
        
}