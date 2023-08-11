from npPirata import multMV, multMM, dot, vectorNegative, normVector

def vertexShader(vertex, **kwargs):
    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    projectionMatrix = kwargs["projectionMatrix"]
    vpMatrix = kwargs["vpMatrix"]

    vt = [vertex[0], 
        vertex[1], 
        vertex[2], 
        1]

    matrix = multMM([vpMatrix, projectionMatrix, viewMatrix, modelMatrix])
    
    vt = multMV(matrix, vt)

    vt = [vt[0] / vt[3],
        vt[1] / vt[3],
        vt[2] / vt[3]]

    return vt

def fragmentShader(**kwargs):
    texCoords = kwargs["texCoords"]
    texture = kwargs["texture"]
    
    if (texture != None):
        color = texture.getColor(texCoords[0], texCoords[1])
    else:
        color = (1, 1, 1)

    return color

def flatShader(**kwargs):
    """ dLight = kwargs["dLight"]
    normal= kwargs["triangleNormal"]

    dLight= vectorNegative(dLight)
    intensity= dot(normal, dLight)

    color = [0, 0, 0]
    color[0] *= intensity
    color[1] *= intensity
    color[2] *= intensity

    if intensity > 0:
        return color

    else:
        return [0,0,0] """

    
    dLight = kwargs["dLight"]
    normal= kwargs["triangleNormal"]
    texCoords = kwargs["texCoords"]
    texture = kwargs["texture"]

    b= 1.0
    g= 1.0
    r= 1.0

    if texture != None:
        textureColor = texture.getColor(texCoords[0], texCoords[1])    
        b *= textureColor[2]
        g *= textureColor[1]
        r *= textureColor[0]

    dLight= vectorNegative(dLight)
    intensity= dot(normal, dLight)
    
    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b

    else:
        return [0,0,0]


def gouradShader(**kwargs):
    tA, tB, tC = kwargs["texCoords"]
    texture = kwargs["texture"]
    nA, nB, nC = kwargs["normals"]
    u, v, w = kwargs["bCoords"]
    dLight = kwargs["dLight"]

    b= 1.0
    g= 1.0
    r= 1.0

    if texture != None:
        tU= u * tA[0] + v * tB[0] + w * tC[0]
        tV= u * tA[1] + v * tB[1] + w * tC[1]
        
        textureColor = texture.getColor(tU, tV)    
        b *= textureColor[2]
        g *= textureColor[1]
        r *= textureColor[0]

    normal= [u * nA[0] + v * nB[0] + w * nC[0],
             u * nA[1] + v * nB[1] + w * nC[1],
             u * nA[2] + v * nB[2] + w * nC[2]]
    
    dLight= vectorNegative(dLight)
    intensity= dot(normal, dLight)
    
    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b

    else:
        return [0,0,0]

def customShader(**kwargs):
    tA, tB, tC = kwargs["texCoords"]
    texture = kwargs["texture"]
    nA, nB, nC = kwargs["normals"]
    u, v, w = kwargs["bCoords"]
    dLight = kwargs["dLight"]

    b = 1.0
    g = 1.0
    r = 1.0

    if texture != None:
        tU = u * tA[0] + v * tB[0] + w * tC[0]
        tV = u * tA[1] + v * tB[1] + w * tC[1]
        
        textureColor = texture.getColor(tU, tV)    
        b *= textureColor[2]
        g *= textureColor[1]
        r *= textureColor[0]

    normal = [u * nA[0] + v * nB[0] + w * nC[0],
              u * nA[1] + v * nB[1] + w * nC[1],
              u * nA[2] + v * nB[2] + w * nC[2]]
    
    dLight = vectorNegative(dLight)
    intensity = dot(normal, dLight)
    
    #b *= intensity
    #g *= intensity
    #r *= intensity

    grayscale_value = (r + g + b) / 3.0

    return grayscale_value, grayscale_value, grayscale_value

    if intensity > 0:
        r = 1 - r
        b = 1 - b
        g = 1 - g
        return r, g, b

    else:
        return [0, 0, 0]

def metallicShader(**kwargs):
    viewDir = normVector(vectorNegative(kwargs["viewDir"]))
    lightDir = normVector(vectorNegative(kwargs["lightDir"]))
    normal = kwargs["normal"]

    # Cálculo de reflexión especular usando el modelo de Phong
    specular_intensity = dot(reflect(lightDir, normal), viewDir) ** 32  # Exponente de brillo ajustable

    # Valores para los canales de color
    r = 0.8 + 0.2 * specular_intensity  # Componente roja con reflexión especular
    g = 0.8 + 0.2 * specular_intensity  # Componente verde con reflexión especular
    b = 0.8 + 0.2 * specular_intensity  # Componente azul con reflexión especular

    return r, g, b

def reflect(v, n):
    dot_product = 2 * dot(v, n)
    return subtractVectors([v, multVectorScalar(n, dot_product)])


