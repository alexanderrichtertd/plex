light test_light(
    float intensity = 1;
    color lightcolor = 1;
    )
{
    vector dir = vector "shader" (0,0,1);
	solar(dir, 0.0)
    {
		Cl = lightcolor * intensity;
	}
}
