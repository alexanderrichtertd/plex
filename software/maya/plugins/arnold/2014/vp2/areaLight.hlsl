cbuffer ConstantBuffer : register(b0)
{
    matrix w : WorldViewProjection;
    matrix vp : WorldViewProjection;
    float4 color = float4(0.8, 0.2, 0.0, 1.0);
}

void mainVS(
    float4 vertex : POSITION,
    out float4 position: SV_POSITION)
{ 
    position = mul(mul(vertex, w), vp);
}

float4 mainPS() : SV_Target
{
    return color;
}
