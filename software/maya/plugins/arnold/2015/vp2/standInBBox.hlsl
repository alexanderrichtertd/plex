cbuffer ConstantBuffer : register(b0)
{
    matrix wvp : WorldViewProjection;
    float4 scale = float4(1.0, 1.0, 1.0, 1.0);
    float4 offset = float4(1.0, 1.0, 1.0, 0.0);
    float4 color = float4(0.8, 0.2, 0.0, 1.0);
}

void mainVS(
    float4 vertex : POSITION,
    out float4 position: SV_POSITION)
{ 
    position = mul(vertex * scale + offset, wvp);
}

float4 mainPS() : SV_Target
{
    return color;
}
