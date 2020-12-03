float map(in vec3 pos)
{
    float d = length(pos)-0.25;
    return d;
    
}


void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    // Normalized pixel coordinates (from 0 to 1)
    vec2 p = (2.0*fragCoord-iResolution.xy)/iResolution.y;
	vec3 ro = vec3(0.0,0.0,2.0);	//ray origion(camera)
    vec3 rd = normalize(vec3(p,-1.5));
    vec3 col = vec3(0.2,0.5,0.8);
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
        col = vec3(1.0);
    }
    // Output to screen
    fragColor = vec4(col,1.0);
        
        
}