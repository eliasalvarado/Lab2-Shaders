from npPirata import multMV, multMM, dot, vectorNegative, normVector, multVectorScalar, subtractVectors

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
    dLight = kwargs["dLight"]
    normal= kwargs["normals"]
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
    textures = kwargs["textures"]
    nA, nB, nC = kwargs["normals"]
    u, v, w = kwargs["bCoords"]
    dLight = kwargs["dLight"]

    b= 1.0
    g= 1.0
    r= 1.0

    for texture in textures:
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


def multiTextureShader(**kwargs):
    tA, tB, tC = kwargs["texCoords"]
    textures = kwargs["textures"]
    u, v, w = kwargs["bCoords"]

    b = 0
    g = 0
    r = 0

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

    return r, g, b

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

    viewDir = [viewDir[0][2],
                viewDir[1][2],
                viewDir[2][2]]

    dot_product = dot(normal, viewDir)

    if dot_product <= 0:
        dot_product = 0
    
    # Ajusta el nivel de opacidad basado en el producto de punto
    # Si la normal está viendo hacia la cámara, se reduce la opacidad
    opacity = 1.0 - max(0.0, dot_product)

    r = 0.5 * opacity
    g = 0.5 * opacity
    b = 0.5 * opacity

    return r, g, b


def heightColorShader(**kwargs):
    A, B, C = kwargs["vertex"]
    camMatrix = kwargs["camMatrix"]

    vt = [min(A[0], B[0], C[0]),
            min(A[1], B[1], C[1]),
            min(A[2], B[2], C[2]),
            1]

    vt = multMV(camMatrix, vt)

    vt = [vt[0] / vt[3],
            vt[1] / vt[3],
            vt[2] / vt[3]]

    # Normaliza la coordenada Z para que esté en el rango [0, 1]
    normalized_z = (vt[2] + 1) / 2

    # Interpola entre el color azul y rojo basado en la coordenada Z
    r = normalized_z
    g = 0
    b = 1 - normalized_z

    return r, g, b

