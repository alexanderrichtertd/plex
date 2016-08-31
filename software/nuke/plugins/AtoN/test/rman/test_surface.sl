surface test_surface(
    color Cd = 1.; 
    float Kd = .18;
    output varying point __Pworld = 0;
    output varying normal __Nworld = 0;
)
{
    normal Nn = normalize(N);
    vector V = normalize(-I);
 
    color _C = 0;
    _C += Cd * Kd * diffuse(Nn);
 
    Ci = _C;
    __Pworld = transform( "world", P );
    __Nworld = ntransform( "world", Nn );
 
    Oi = 1;
    Ci *= Oi;
}
