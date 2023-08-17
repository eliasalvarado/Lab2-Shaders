from npPirata import multMV, multMM, dot, vectorNegative, normVector, multVectorScalar, subtractVectors, reflectVector, invertMatrix
from random import random

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

def emptyBlocksVertexShader(vertex, **kwargs):
    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    projectionMatrix = kwargs["projectionMatrix"]
    vpMatrix = kwargs["vpMatrix"]
    height = kwargs["height"]

    vt = [vertex[0], 
        vertex[1], 
        vertex[2], 
        1]

    matrix = multMM([vpMatrix, projectionMatrix, viewMatrix, modelMatrix])
    
    vt = multMV(matrix, vt)

    vt = [vt[0] / vt[3],
        vt[1] / vt[3],
        vt[2] / vt[3]]

    bloques = []

    for i in range(0, height, 50):
        bloques.append((i, i + 15))

    y = round(vt[1])
    if any(start <= y <= end for start, end in bloques):
        return None

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
    tA, tB, tC = kwargs["texCoords"]
    textures = kwargs["textures"]
    nA, nB, nC = kwargs["normals"]
    u, v, w = kwargs["bCoords"]
    dLight = kwargs["dLight"]
    viewDir = kwargs["camMatrix"]

    normal = [u * nA[0] + v * nB[0] + w * nC[0],
             u * nA[1] + v * nB[1] + w * nC[1],
             u * nA[2] + v * nB[2] + w * nC[2]]


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

def heightColorShader(**kwargs):
    tA, tB, tC = kwargs["texCoords"]
    textures = kwargs["textures"]
    nA, nB, nC = kwargs["normals"]
    u, v, w = kwargs["bCoords"]
    dLight = kwargs["dLight"]
    viewDir = kwargs["camMatrix"]
    A, B, C = kwargs["vertex"]
    vCoords = kwargs["vCoords"]

    normal = [u * nA[0] + v * nB[0] + w * nC[0],
             u * nA[1] + v * nB[1] + w * nC[1],
             u * nA[2] + v * nB[2] + w * nC[2]]

    viewDir = [viewDir[0][1],
                viewDir[1][1],
                viewDir[2][1]]
    
    normal = normVector(normal)

    intensity = dot(normal, dLight)
    intensity = max(0, min(intensity, 1))

    viewDir = vectorNegative(viewDir)
    reflection = reflectVector(dLight, normal)
    specIntensity = dot(viewDir, reflection)
    
    specIntensity = max(0, min(specIntensity, 1))

    r = b = g = specIntensity

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
            height_factor = (normal[0] + normal[1] + normal[2]) / 3.0
            r += max(0, min(1, textureColor[0] + height_factor))
            g += textureColor[1]
            b += max(0, min(1, textureColor[2] - height_factor))

    r /= len(textures)
    g /= len(textures)
    b /= len(textures)

    r *= opacity
    g *= opacity
    b *= opacity

    if (r > 1): r = 1
    if (g > 1): g = 1
    if (b > 1): b = 1

    return r, g, b

def neonShader(**kwargs):
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

    normal = normVector(normal)

    intensity = dot(normal, dLight)
    intensity = max(0, min(intensity, 1))

    viewDir = vectorNegative(viewDir)
    reflection = reflectVector(dLight, normal)
    specIntensity = dot(viewDir, reflection)
    specIntensity = max(0, min(specIntensity, 1))

    r = b = g = specIntensity

    for texture in textures:
        if texture != None:
            tU = u * tA[0] + v * tB[0] + w * tC[0]
            tV = u * tA[1] + v * tB[1] + w * tC[1]
            
            textureColor = texture.getColor(tU, tV)    
            r += textureColor[0] * 2
            g += textureColor[1] * 2
            b += textureColor[2] * 2

    r /= len(textures)
    g /= len(textures)
    b /= len(textures)

    if r > 1: r = 1
    if g > 1: g = 1
    if b > 1: b = 1

    return r, g, b

def metallicShader(**kwargs):
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

    normal = normVector(normal)

    intensity = dot(normal, dLight)
    intensity = max(0, min(intensity, 1))

    viewDir = vectorNegative(viewDir)
    reflection = reflectVector(dLight, normal)
    specIntensity = dot(viewDir, reflection)
    
    specIntensity = max(0, min(specIntensity, 1))

    r = g = b = 0

    for texture in textures:
        if texture != None:
            tU= u * tA[0] + v * tB[0] + w * tC[0]
            tV= u * tA[1] + v * tB[1] + w * tC[1]
            
            textureColor = texture.getColor(tU, tV)  
            base_color = [textureColor[0], textureColor[1], textureColor[2]]  
            r += base_color[0] * (1 - specIntensity) + specIntensity
            g += base_color[1] * (1 - specIntensity) + specIntensity
            b += base_color[2] * (1 - specIntensity) + specIntensity

    r /= len(textures)
    g /= len(textures)
    b /= len(textures)

    if (r > 1): r = 1
    if (g > 1): g = 1
    if (b > 1): b = 1

    return r, g, b
