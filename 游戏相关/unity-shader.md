
# Shader基础

## 基础的shader模板

```c#
Shader "ShaderName" {
  Properties {
  
  }
  SubShader {
    //针对显卡A的SubShader
    Pass {
            //设置渲染状态和标签
            
            CGPROGRAM

            #pragma vertex vert_main
            #pragma fragment frag_main
            
            float4 vert_main(float4 v: POSITION) : SV_POSITION {
              return mul(UNITY_MATRIX_MVP, v);
            }
            
            fixed4 frag_main() : SV_Target {
              return fixed4(1.0, 1.0, 1.0, 1.0);
            }

            ENDCG

            //其他设置
        }
        Pass {
            //其他Pass
        }
  }
  SubShader {
    //针对显卡B的SubShader
  }
  Fallback "VertexLit"
}
```

## 使用结构体

```c#
Shader "ShaderName" {
  SubShader {
    CGPROGRAM
    
    #pragma vertex vertex_main
    #pragma fragment frag_main
    
    //application to vertex
    struct a2v {
      float4 vertex: POSITION;
      float3 normal: NORMAL;
      float4 texcoord: TEXCOORD0;
    };
    
    //vertex to fragment
    struct v2f {
      float4 pos: SV_POSITION;
      fixed3 color: COLOR0;
    };
    
    v2f vertex_main(a2v v): SV_POSITION {
      v2f o;
      o.pos = mul(UNITY_MATRIX_MVP, v.vertex);
      o.color = v.normal * 0.5 + fixed3(0.5, 0.5, 0.5);
      return o;
    }
    
    fixed4 frag_main(v2f i): SV_Target {
      return fixed4(i.color, 1.0);
    }
    
    CGEND
  }
}
```

## 使用Properties

```c
//定义属性
Properties {
  //属性名 ("属性描述", 属性类型) = 默认值
  _Color ("Color Tint", Color) = (1.0, 1.0, 1.0, 1.0)
}

//使用属性
fixed4 frag_main(v2f i): SV_Target {
  fixed3 c = i.color;
  c *= _Color.rgb;
  return fixed4(c, 1.0);
}
```

各种属性

| ShaderLab属性类型 |       CG类型        |
| :---------------: | :-----------------: |
|   Color,Vector    | float4,half4,fixed4 |
|    Range,Float    |  float,half,fixed   |
|        2D         |      sampler2D      |
|       Cube        |     samplerCube     |
|        3D         |      sampler3D      |

## 使用语义

每个语义代表一个寄存器，表明这个变量存放在哪个寄存器。

寄存器之间没有真正含义的区分，只有一些约定俗称的含义。所以可以使用任意寄存器，传递任意含义的数据。

**application to vert_main**

| 语义        | 描述                 | 类型          |
| ----------- | -------------------- | ------------- |
| POSITION    | 模型空间中顶点位置。 | float4        |
| NORMAL      | 顶点法线。           | float3        |
| TANGENT     | 顶点切线。           | float4        |
| TEXCOORD(n) | 纹理坐标。           | float2/float4 |
| COLOR       | 顶点颜色。           | fixed4/float4 |

**vert_main to frag_main**

| 语义        | 描述                 | 类型   |
| ----------- | -------------------- | ------ |
| SV_POSITION | 裁剪空间中的顶点坐标 | float4 |
| TEXCOORD(n) | 纹理坐标             | float4 |
| COLOR0      | 第一组顶点颜色       |        |
| COLOR1      | 第二组顶点颜色       |        |

**frag_main output**

| 语义      | 描述                      | 类型   |
| --------- | ------------------------- | ------ |
| SV_Target | 存储到render target的颜色 | float4 |

## CG数据类型

| 类型  |         精度          |
| :---: | :-------------------: |
| float |      32位浮点数       |
| half  | 16位浮点数。(-6w, 6w) |
| fixed |  11位浮点数。(-2, 2)  |

## 设置ShaderTarget

```c++
#pragma target 2.0
```

## 使用Unity自带的文件

**使用**

```c++
CGPROGRAM
#include "UnityCG.cginc"
CGEND
```

**位置**

<Unity安装路径>/Data/CGIncludes

**列表**

|           文件名           |                          描述                          |
| :------------------------: | :----------------------------------------------------: |
|       UnityCG.cginc        |            包含了最常用的函数，宏，结构体。            |
| UnityShaderVariables.cginc | 会自动包含进来，包含内置的全局变量，如UNITY_MATRIX_MVP |
|       Lighting.cginc       | 包含很多内置的光照模型，编译Surface Shader时会自动包含 |
|     HLSLSupport.cginc      |       会自动 包含进来，包含跨平台编译的宏和定义        |

## 使用Unity宏

```c++
//用于表面着色器，初始化输出参数到默认值。
void vert(inout appdata_full v, out Input o) {
  UNITY_INITIALIZE_OUTPUT(Input, o);
}
```

## 内置变量

| 变量名                   | 变量类型        | 备注   |
| ------------------------ | --------------- | ------ |
| UNITY_LIGHTMODEL_AMBIENT | float4(x,y,z,w) | 环境光 |
|                          |                 |        |

## 内置结构体

```c#
struct appdata_base {
  float4 vertex: POSITION;
    float3 normal: NORMAL;
    float4 texcoord: TEXCOORD0;
};

struct appdata_tan {
  float4 vertex: POSITION;
  float4 tangent: TANGENT;
  float3 normal: NORMAL;
  float4 texcoord: TEXCOORD0;
};

struct appdata_full {
  float4 vertex: POSITION;
  float4 tangent: TANGENT;
  float3 normal: NORMAL;
    float4 texcoord : TEXCOORD0;
    float4 texcoord1 : TEXCOORD1;
    float4 texcoord2 : TEXCOORD2;
    float4 texcoord3 : TEXCOORD3;
    fixed4 color : COLOR;
};

//可用于定点着色器的输出
struct v2f_img {
  float4 pos: SV_POSITION;
  half2 uv: TEXCOORD0;
}
```

## 内置函数

```c#
//vertex: 顶点位置(模型空间)
//ret: 世界空间中，由顶点指向相机的方向向量
float3 WorldSpaceViewDir(float4 vertex);
//ret: 模型空间中，由顶点指向相机的方向向量
float3 ObjSpaceViewDir(float4 vertex);
//还有对应的输入世界空间中顶点位置的版本
float3 UnityWorldSpaceViewDir(float4 vertexWorld);
float3 UnityObjSpaceViewDir(float4 vertexWorld);

//只能用于前向渲染
//vertex: 顶点位置(模型空间)
//ret: 世界空间中，该点到光源的方向向量
float3 WorldSpaceLightDir(float4 vertex);
//ret: 模型空间中，该点到光源的方向向量
float3 ObjSpaceLightDir(float4 vertex);
float3 UnityWorldSpaceLightDir(float4 vertexWorld);
float3 UnityObjSpaceLightDir(float4 vertexWorld);

//把法线方向从模型空间转换到世界空间。已归一化。
float3 UnityObjectToWorldNormal(float3 norm);
//把方向矢量从模型空间转换到世界空间。已归一化。
float3 UnityObjectToWorldDir(float3 dir);
//把方向矢量从世界空间转换到模型空间。已归一化。
float3 UnityWorldToObjectDir(float3 dir);

//求反射向量
//i：其中一个向量，由表面指向远方
//n：表面法线
float4 reflect(float4 i, float4 n);

//将x截取在[0,1]范围。
//如果x是矢量，则对每个分量都进行截取。
float saturate(float x);
```

# 光照

## 计算理论

* 光照的过程，就是给定输入，计算物体最终颜色的过程。
* 这个过程，称为着色。每种着色方式，称为一种光照模型。
* 每种光照模型，通常都会用一个等式来表达：`ObjColor=Func(Light, ObjMaterial, Camera)`
* 不同的光照模型，用于模拟不同表面的物体，例如粗糙的木质表面，光滑的金属表面等。

## 三个输入口

### 光源

> 光源有三个属性，通过光源发出的光线来表现
>
> * 光线密度
>
> * 光线颜色
>
> * 光线方向

### 被照射物体

> 光线到达物体后，会有 两种结果：
>
> * 散射：只改变光线方向，不改变光线密度和颜色。光线经散射后，有两种结果：
>   * 一种会散射到内部，称为**折射**
>     * 对于不透明的物体，折射到内部的光线，还会再射出表面，称为**次表面反射**
>   * 另一种散射到外部，称为**反射**
> * 吸收：改变光线密度和颜色，不改变光线方向。等于这部分光被物体吞噬了。

### 摄像机

> 物体的光照结果，等于最终到达摄像机的光线属性。

## 光照模型的分类

### 按是否符合真实世界来分

* 真实模型：完全真实地模拟光线与物体之间的交互过程
* 经验模型：对真实模型理想化和简化的结果
* 基于物理的光照模型：比真实模型简单，比经验模型复杂

### 按计算内容来分

* 只计算直接光照
* 同时计算直接光照与间接光照

### 什么是直接光照

* 光线由光源发出后到达物体，经物体一次反射直接进入摄像机的光线。

### 按使用哪种着色器来分

* 顶点光照：在顶点着色器中计算光照、
  * 计算量会稍小，因为顶点数量一般小于片元数量。
  * 但由于顶点间的距离可能会很大，所以计算结果经差值后往往不准确，某些情况下可能会有棱角。
* 像素光照：在片元着色器中计算光照
  * 计算量会稍大。

## 标准光照模型

### 理论基础

> 经验模型。主要关心直接光照，间接光照计算由简单的模拟代替。

> 标准光照模型把进入到摄像机的光线，分为4个部分，每个部分使用不同的方法来计算，最终颜色为4个部分的简单叠加。

> 1. 环境光（ambient）：用于模拟间接光照，如于老师的脸被帽子映绿的情景。
>
> 2. 自发光（emissive）：用于模拟光源的光直接进入摄像机的部分。
>
> 3. 漫反射（diffuse）：入射光线经漫反射后，会向各个方向均匀反射。
>
>    > `DiffuseColor=(LightColor*MaterialDiffuseColor)*max(0, normal * lightDir)`
>    >
>    > 其中，normal为表面法线，lightDir为物体指向光源的单位矢量。
>
>    > 上面使用的模型称为兰伯特模型，但是有个缺点，由于强行截断`normal*lightDir`的值，导致背光面一团黑。
>    >
>    > 半兰伯特模型可以解决这个问题：
>    >
>    > `DiffuseColor=(LightColor*MaterialDiffuseColor)*(0.5*(normal*lightDir)+0.5)`
>
> 4. 高光反射（specular）：Phong模型
>
>    > `SpecularColor=(LightColor * MaterialSpecularColor) * max(0, viewDir * reflectDir)^gloss`
>    >
>    > 其中，viewDir是物体到摄像机的方向向量，gloss与高光区域的大小成反比，reflectDir是光线反射方向。
>    >
>    > 反射方向可以由`reflectDir=2*(normal*lightDir)*normal-lightDir`计算

计算高光反射的另一种方式——Blinn模型

> 最终颜色`DiffuseColor=(LightColor*MaterialDiffuseColor)*max(0, normal * h)^gloss`
>
> 其中`h = normalize(viewDir + lightDir)`

标准光照模型的缺点

> 很多物理现象无法模拟，例如菲涅尔反射。
>
> Blinn-Phong模型是各项同性的，也就是固定视角和光源方向时，旋转物体表面，反射不会发生改变。

技术选择

> 一般情况下，漫反射使用半兰伯特模型，高光反射使用Blinn模型。

### Unity-顶点shader

```c
Shader "StandardLightingModel VertexShader" {
    Properties {
      _Emissive ("自发光颜色", Color) = (0.0, 0.0, 0.0, 0.0)

        _Diffuse ("漫反射颜色", Color) = (1.0, 1.0, 1.0, 1.0)

        _Specular("高光反射颜色", Color) = (1.0, 1.0, 1.0, 1.0)
        _Gloss("高光斑点", Range(8, 256)) = 20
    }
    SubShader {
        Pass {
            Tags {
                "LightMode" = "ForwardBase"
            }
            CGPRAGMA
            
            #pragma vertex vert_main
            #pragma fragment frag_main
            #include "Lighting.cginc"
                
            fixed4 _Emissive;
            fixed4 _Diffuse;
            fixed4 _Specular;
            float _Gloss;
            
            struct v2f {
              float4 pos: SV_POSITION;
              fixed3 color: COLOR;
            };

            v2f vert_main(appdata_base v): SV_POSITION {
              v2f o;
              o.pos = mul(UNITY_MATRIX_MVP, v.vertex);

              //环境光
              fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT.xyz;

              //自发光
              fixed3 emissive = _Emissive.rgb;

              fixed3 worldNormal = UnityObjectToWorldNormal(v.normal);
              fixed3 lightDir = normalize(_WorldSpaceLightPos0.xyz);
              fixed3 viewDir = normalize(WorldSpaceViewDir(v.vertex));
                
              //漫反射
              float diffuse_factor = (worldNormal * lightDir) * 0.5 + 0.5;
              fixed3 diffuse = _LightColor0.rgb * _Diffuse.rgb * diffuse_factor;

              //镜面反射
              fixed3 h = normalize(viewDir + lightDir);
              float specular_factor = pow(max(0, dot(worldNormal, h)), _Gloss);
              fixed3 specular = _LightColor0.rgb * _Specular.rgb * specular_factor;

              //叠加4种颜色
              o.color = ambient + emissive + diffuse + specular;

              return o;
            }

            fixed4 frag_main(v2f i): SV_Target {
              return fixed4(i.color, 1.0);
            }
            
            ENDCG
        }
    }
}
```

### Unity-像素shader

```c
Shader "StandardLightModel PixelShader" {
  Properties {
      _Emisive ("自发光颜色", Color) = (0.0, 0.0, 0.0, 0.0)

        _Diffuse ("漫反射颜色", Color) = (1.0, 1.0, 1.0, 1.0)

        _Specular("高光反射颜色", Color) = (1.0, 1.0, 1.0, 1.0)
        _Gloss("高光斑点", Range(8, 256)) = 20
  }
  SubShader {
    Pass {
      Tags {
                "LightMode" = "ForwardBase"
            }
            CGPRAGMA
            
            #pragma vertex vert_main
            #pragma fragment frag_main
            #include "Lighting.cginc"

            fixed4 _Emissive;
            fixed4 _Diffuse;
            fixed4 _Specular;
            float _Gloss;
            
            struct v2f {
              float4 pos: SV_POSITION;
              fixed3 worldNormal: TEXCOORD0;
              fixed3 viewDir: TEXCOORD1;
            }
            
            v2f vert_main(appdata_base v) {
              v2f o;
              o.pos = mul(UNITY_MATRIX_MVP, v.vertex);
              o.worldNormal = UnityObjectToWorldNormal(v.normal);
              o.viewDir = normalize(WorldSpaceViewDir(v.vertex));
              return o;
            }
            
            fixed4 frag_main(v2f i): SV_Target {
              //环境光
              fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT.xyz;

              //自发光
              fixed3 emissive = _Emissive.rgb;

              fixed3 worldNormal = i.worldNormal;
              fixed3 lightDir = normalize(_WorldSpaceLightPos0.xyz);
              fixed3 viewDir = i.viewDir;

              //漫反射
              float diffuse_factor = saturate(0, worldNormal * lightDir);
              fixed3 diffuse = _LightColor0.rgb * _Diffuse.rgb * diffuse_factor;

              //镜面反射
              float3 h = normalize(viewDir * lightDir);
              float specular_factor = pow(max(0, worldNormal*h), _Gloss);
              fixed3 specular = _LightColor0.rgb * _Specular.rgb * specular_factor;

              //叠加4种颜色
              fixed3 color = saturate(ambient + emissive + diffuse + specular);

              return fixed4(color, 1.0);
            }
            
            CDEND
    }
  }
}
```

# 纹理

## 理论基础

* OpenGL和Unity中，纹理原点在左下角；DirectX中，纹理坐标在左上角。

## 单张纹理

普通的贴图纹理，一般用于替换漫反射计算时的物体颜色。

### Shader实现

```c
Shader "MyShader" {
  Properties {
    _Color("Color Tint", Color) = (1, 1, 1, 1)
    _MainTex("Main Tex", 2D) = "white" {}
  }
  SubShader {
    Pass {
      Tags {
        "LightMode" = "ForwardBase"
      }
      
      CGPROGRAM
      #pragma vertex vert_main
      #pragma fragment frag_main
      #include "Lighting.cginc"
      
      fixed4 _Color;
      sampler2D _MainTex;
      float4 _MainTex_ST;
      
      struct v2f {
        fixed4 pos: SV_POSITION;
        float2 uv: TEXCOORD0;
        fixed3 worldNormal: TEXCOORD1;
      };
      
      v2f vert_main(appdata_base v) {
        v2f o;
        o.pos = mul(UNITY_MATRIX_MVP, v.vertex);
        o.worldNormal = UnityObjectToWorldNormal(v.normal);
        o.uv = TRANSFORM_TEX(v.texcoord, _MainTex);
        return o;
      }
      
      fixed4 frag_main(v2f i) {
        fixed3 albedo = tex2D(_MainTex, i.uv).rgb * _Color.rgb;
          
        fixed3 worldNormal = i.worldNormal;
        fixed3 lightDir = normalize(_WorldSpaceLightPos0.xyz);

        //漫反射
        float diffuse_factor = saturate(0, worldNormal * lightDir);
        fixed3 diffuse = _LightColor0.rgb * albedo * diffuse_factor;
          
        return fixed4(diffuse, 1.0);
      }
      CDEND
    }
  }
}
```

### 纹理属性

* WrapMode：决定了当纹理坐标超过[0,1]时如何平铺
  * Repeat：整数部分被舍弃，相当于做了取余操作。
  * Clamp：强制截取到[0,1]，相当于一直重复边界。
* FilterMode：当纹理被缩放时，使用哪种算法得到目标像素
  * Point：只使用最近的像素得到目标像素。
  * Bilinear：使用最近的4个像素得到目标像素。
  * Trilinear：在Bilinear的基础上，同时使用mipmap。
* mipmap：多级渐远纹理
  * 需要先在面板上将**纹理类型**调整为**Advanced**，再勾选**Generate Mip Maps**
* 最大尺寸：不同的平台支持的纹理最大尺寸都不一样，所以需要选择一个合适的值
  * 如果导入的纹理超过了最大尺寸，Unity会将其缩放到最大尺寸。

## 凹凸映射

进行凹凸映射由两种方法

* 高度纹理
  * 高度图存储了表面的高低程度，用灰度图就可以。
  * 优点是比较直观，缺点是计算量更大一点。
* 法线纹理
  * 由于法线的每个分量在[-1,1]范围，纹理范围为[0,1]，所以会有一个映射关系
    * 法线到纹理：`Pixel.rgb = (Normal.xyz + 1) / 2`
    * 纹理到法线：`Normal.xyz = Pixel.rgb * 2 - 1`
  * 法线纹理也分两种
    * 模型空间的法线纹理：记录的是模型空间下，每个顶点的绝对法线信息。
      * 由于记录的是绝对的法线信息，所以不需要模型自带法线信息
      * 在纹理坐标的结合处或模型边缘尖锐部分，可以更平滑。因为插值时都在模型空间做。
    * 切线空间的法线纹理：记录的是每个顶点的切线空间下，法线方向。
      * 可以进行平滑的UV动画。
      * 可以将一个面的法线纹理用在另一个面上，模型空间的法线纹理就做不到这样。
      * 可压缩：只存储XY值，运行时求出Z值。

### 在切线空间计算

```c
Shader "MyShader" {
  Properties {
    _MainTex("MainTex", 2D) = "white" {}
    _BumpTex("BumpTex", 2D) = "bump" {}
    _BumpScale("BumpScale", Float) = 1.0
        _Specular("高光反射颜色", Color) = (1.0, 1.0, 1.0, 1.0)
        _Gloss("高光斑点", Range(8, 256)) = 20
  }
  SubShader {
    Pass {
      Tags {
        "LightMode" = "ForwardBase"
      }
      CGPROGRAM
      #pragma vertex vert_main
      #pragma fragment frag_main
      #include "Lighting.cginc"
      
      sample2D _MainTex;
      float4 _MainTex_ST;
      sample2D _BumpTex;
      float4 _BumpTex_ST;
      float _BumpScale;
      fixed4 _Specular;
      float _Gloss;
      
      struct v2f {
        float4 pos: SV_POSITION;
        float4 uv: TEXCOORD0;
        float3 lightDirInTangent: TEXCOORD1;
        float3 viewDirInTangent: TEXCOORD2;
      };
      
      v2f vert_main(appdata_tan v) {
        v2f o;
        o.pos = mul(UNITY_MATRIX_MVP, v.vertex);
        
        o.uv.xy = TRANSFORM_TEX(v.texcoord, _MainTex);
        o.uv.zw = TRANSFORM_TEX(v.texcoord, _BumpTex);
        
        fixed3 worldNormal = UnityObjectToWorldNormal(v.normal);  
        fixed3 worldTangent = UnityObjectToWorldDir(v.tangent.xyz);  
        fixed3 worldBinormal = cross(worldNormal, worldTangent) * v.tangent.w; 
        float3x3 worldToTangent = float3x3(worldTangent, worldBinormal, worldNormal);
        
        o.lightDirInTangent = mul(worldToTangent, WorldSpaceLightDir(v.vertex));
        o.viewDirInTangent = mul(worldToTangent, WorldSpaceViewDir(v.vertex));
        
        return o;
      }
      
      fixed4 frag_main(v2f i): SV_Target {
      
        //主贴图
        fixed3 albedo = tex2D(_MainTex, i.uv.xy).rgb * _Color.rgb;
        
        //切线空间下的法向量
        fixed3 tangentNormal = tex2D(_BumpTex, i.uv.zw).rgb;
        tangentNormal = unpackNormal(tangentNormal);
        tangentNormal.xy *= _BumpScale;
        tangentNormal.z = sqrt(1.0 - saturate(dot(tangentNormal.xy, tangentNormal.xy)));

        //切线空间下的反光线
        fixed3 tangentLightDir = normalize(i.lightDirInTangent);

        fixed3 diffuse = _LightColor0.rgb * albedo * max(0, dot(tangentNormal, tangentLightDir));
        
        float3 h = normalize(i.viewDirInTangent * tangentLightDir);
        float specular_factor = pow(max(0, tangentNormal*h), _Gloss);
        fixed3 specular = _LightColor0.rgb * _Specular.rgb * specular_factor;
        
        return fixed4(diffuse+specular, 1.0);
      }
      
      ENDCG
    }
  }
}
```

### 在世界空间计算

```c
Shader "MyShader" {
  Properties {
      _MainTex("MainTex", 2D) = "white" {}
      _BumpTex("BumpTex", 2D) = "bump" {}
      _BumpScale("BumpScale", Float) = 1.0
      _Specular("Specular", Color) = (1, 1, 1, 1)
      _Gloss("Gloss", Float) = 20
  }
  SubShader {
    Pass {
      Tags {
        "LightMode" = "ForwardBase"
      }
      CGPROGRAM
      #pragma vertex vert_main
      #pragma fragment frag_main
      #include "Lighting.cginc"

      sample2D _MainTex;
      float2 _MainTex_ST;
      sample2D _BumpTex;
      float2 _BumpTex_ST;
      fixed4 _Specular;
      float _Gloss;

      struct v2f {
        float4 pos: SV_POSITION;
        float4 uv: TEXCOORD0;
        float4 TtoW0 : TEXCOORD1;
        float4 TtoW1 : TEXCOORD2;
        float4 TtoW2 : TEXCOORD3;
      };

      v2f vert_main(appdata_tan v) {
        v2f o;
        o.pos = mul(UNITY_MATRIX_MVP, v.vertex);
        o.uv.xy = TRANSFORM_TEX(o.texcoord, _MainTex);
        o.uv.zw = TRANSFORM_TEX(o.texcoord, _BumpTex);

        float3 worldPos = mul(_Object2World, v.vertex).xyz;
        fixed3 worldNormal = UnityObjectToWorldNormal(v.normal);
        fixed3 worldTangent = UnityObjectToWorldDir(v.tangent.xyz);
        fixed3 worldBinormal = cross(worldNormal, worldTangent) * v.tangent.w;
        
        o.TtoW0 = float4(worldTangent.x, worldBinormal.x, worldNormal.x, worldPos.x);
        o.TtoW1 = float4(worldTangent.y, worldBinormal.y, worldNormal.y, worldPos.y);
        o.TtoW2 = float4(worldTangent.z, worldBinormal.z, worldNormal.z, worldPos.z);

        return o;
      }

      fixed4 frag_main(v2f i): SV_Target {

        fixed3 lightDir = i.lightDir;

        float3 bump = unpackNormal(tex2D(_BumpTex, i.uv.zw));
        bump.xy *= _BumpScale;
        bump.z = sqrt(1 - bump.xy*bump.xy);
        fixed3 normal = normalize(half3(dot(i.TtoW0.xyz, bump), dot(i.TtoW1.xyz, bump), dot(i.TtoW2.xyz, bump)));

        float3 worldPos = float3(i.TtoW0.w, i.TtoW1.w, i.TtoW2.w);
        fixed3 lightDir = normalize(UnityWorldSpaceLightDir(worldPos));
        fixed3 viewDir = normalize(UnityWorldSpaceViewDir(worldPos));

        fixed3 albedo = tex2D(_MainTex, i.uv.xy);

        float diffuse_factor = (normal * lightDir) * 0.5 + 0.5;
        fixed3 diffuse = _LightColor0.rgb * albedo * diffuse_factor;

        float h = normalize(viewDir + lightDir);
        float specular_factor = pow(max(0, normal * h), _Gloss);
        fixed3 specular = (_LightColor0.rgb * _Specular.rgb) * specular_factor;

        return fixed4(diffuse + specular, 1.0);
      }

      CGEND
    }
  }
}
```



### 纹理属性

* 设置纹理类型为**Normal Map**
* Create from Grayscale：导入高度图时勾选此选项，Unity会将这张高度图转换成切线空间下的法线纹理。
  * Bumpiness：凹凸程度
  * Filtering：过渡效果。Smooth/Sharp

## 渐变纹理