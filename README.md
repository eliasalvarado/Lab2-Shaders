# Lab2-Shaders

Para la creación del Shader de Neón se consultó a ChatGPT para conocer sobre su implementación:
Este fue el promp para la consulta:
utilizando ÚNICAMENTE los parámetros, variables y funciones utilizadas en estos dos shader, quiero que crees un nuevo shader. 

```
def transparentShader(**kwargs):
    tA, tB, tC = kwargs["texCoords"]
    textures = kwargs["textures"]
    nA, nB, nC = kwargs["normals"]
    u, v, w = kwargs["bCoords"]
    dLight = kwargs["dLight"]
    viewDir = kwargs["camMatrix"]

    normal = [u * nA[0] + v * nB[0] + w * nC[0],
             u * nA[1] + v * nB[1] + w * nC[1],
             u * nA[2] + v * nB[2] + w * nC[2]]

    viewDir = [viewDir[0][0],
                viewDir[1][0],
                viewDir[2][0]]

    """ viewDir = [(viewDir[0][1] + viewDir[0][0]) / 2,
                (viewDir[1][1] + viewDir[1][0]) / 2,
                (viewDir[2][1] + viewDir[2][0]) / 2] """

    dot_product = dot(normal, viewDir)

    if dot_product <= 0:
        dot_product = 0
    
    opacity = 1.0 - max(0.0, dot_product)
    
    r = 0
    g = 0
    b = 0

    for texture in textures:
        if texture != None:
            tU= u * tA[0] + v * tB[0] + w * tC[0]
            tV= u * tA[1] + v * tB[1] + w * tC[1]
            
            textureColor = texture.getColor(tU, tV)  
            b += textureColor[2]
            g += textureColor[1]
            r += textureColor[0]

    r /= len(textures)
    g /= len(textures)
    b /= len(textures)

    r *= opacity
    g *= opacity
    b *= opacity

    return r, g, b
```

Su respuesta fue:
Aquí tienes un nuevo shader llamado neonShader basado en los parámetros y funciones proporcionados en los shaders anteriores:
```
def neonShader(**kwargs):
    tA, tB, tC = kwargs["texCoords"]
    textures = kwargs["textures"]
    nA, nB, nC = kwargs["normals"]
    u, v, w = kwargs["bCoords"]
    dLight = kwargs["dLight"]
    viewDir = kwargs["camMatrix"]

    normal = [
        u * nA[0] + v * nB[0] + w * nC[0],
        u * nA[1] + v * nB[1] + w * nC[1],
        u * nA[2] + v * nB[2] + w * nC[2]
    ]

    viewDir = [viewDir[0][2],
                viewDir[1][2],
                viewDir[2][2]]

    normal = normVector(normal)

    intensity = dot(normal, dLight)
    intensity = max(0, min(intensity, 1))

    viewDir = vectorNegative(viewDir)
    reflection = reflectVector(dLight, normal)
    specIntensity = dot(viewDir, reflection)
    specIntensity = max(0, min(specIntensity, 1))

    base_color = [0.0, 0.0, 0.0]  # Color base negro
    specular_color = [1.0, 1.0, 1.0]  # Color especular blanco

    r = base_color[0] * (1 - specIntensity) + specular_color[0] * specIntensity
    g = base_color[1] * (1 - specIntensity) + specular_color[1] * specIntensity
    b = base_color[2] * (1 - specIntensity) + specular_color[2] * specIntensity

    for texture in textures:
        if texture != None:
            tU = u * tA[0] + v * tB[0] + w * tC[0]
            tV = u * tA[1] + v * tB[1] + w * tC[1]
            
            textureColor = texture.getColor(tU, tV)    
            r += textureColor[0] * 2  # Aumenta el componente rojo
            g += textureColor[1] * 2  # Aumenta el componente verde
            b += textureColor[2] * 2  # Aumenta el componente azul

    r /= len(textures)
    g /= len(textures)
    b /= len(textures)

    if r > 1: r = 1
    if g > 1: g = 1
    if b > 1: b = 1

    return r, g, b
```

Este neonShader aumenta los componentes de color (rojo, verde y azul) de la textura de manera más pronunciada, simulando un efecto de iluminación similar al de un letrero de neón brillante. Puedes ajustar los valores multiplicativos en la línea r += textureColor[0] * 2, g += textureColor[1] * 2 y b += textureColor[2] * 2 para obtener el nivel de brillo deseado en cada componente de color.


Utilizando esta respuesta como base, se optó a realizar modificaciones al código proporcionado por la IA y la creación de la operación entre vectores de nombre _reflectVector_
Dicha función fue creada por la misma IA:
![image](https://github.com/eliasalvarado/Lab2-Shaders/assets/77988653/e0ef86de-292a-4ef0-a7df-85a34a5125e8)
```
def reflectVector(vector, normal):
    dot_product = dot(vector, normal)
    reflection = [vector[i] - 2 * dot_product * normal[i] for i in range(len(vector))]
    return reflection
```
