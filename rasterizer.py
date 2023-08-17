from gl import Renderer, Model
import shaders


width = 500
height = 500

scaleDim = 10

#Primer Shader - Manejo de múltiples texturas
rend = Renderer(width, height)
rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.multiTextureShader
rend.glLoadModel(filename = "sword.obj",
                texNames = ["swordtex.bmp", "swordtex1.bmp"],
                translate=(0, 100, -500),
                rotate=(95, 50, 0),
                scale=(scaleDim, scaleDim, scaleDim))
rend.glLookAt(camPos=(0, 0, 0),
                eyePos=(30, 0, -500))
rend.glRender()
rend.glFinish("multipleTextureShader.bmp")


#Segundo Shader - Shader con brillo metálico
rend1 = Renderer(width, height)
rend1.vertexShader = shaders.vertexShader
rend1.fragmentShader = shaders.metallicShader
rend1.glLoadModel(filename = "sword.obj",
                texNames = ["swordtex.bmp", "swordtex1.bmp"],
                translate=(0, 100, -500),
                rotate=(95, 50, 0),
                scale=(scaleDim, scaleDim, scaleDim))
rend1.glLookAt(camPos=(0, 0, 0),
                eyePos=(30, 0, -500))
rend1.glRender()
rend1.glFinish("metallicShader.bmp")


#Tercer Shader - Shader con brillo de neón
rend2 = Renderer(width, height)
rend2.vertexShader = shaders.vertexShader
rend2.fragmentShader = shaders.neonShader
rend2.glLoadModel(filename = "sword.obj",
                texNames = ["swordtex.bmp", "swordtex1.bmp"],
                translate=(0, 100, -500),
                rotate=(95, 50, 0),
                scale=(scaleDim, scaleDim, scaleDim))
rend2.glLookAt(camPos=(0, 0, 0),
                eyePos=(30, 0, -500))
rend2.glRender()
rend2.glFinish("neonShader.bmp")


#Cuarto Shader - Shader con escala de color y nuevo vertex shader
rend3 = Renderer(width, height)
rend3.vertexShader = shaders.emptyBlocksVertexShader
rend3.fragmentShader = shaders.heightColorShader
rend3.glLoadModel(filename = "sword.obj",
                texNames = ["swordtex.bmp", "swordtex1.bmp"],
                translate=(0, 100, -500),
                rotate=(95, 50, 0),
                scale=(scaleDim, scaleDim, scaleDim))
rend3.glLookAt(camPos=(0, 0, 0),
                eyePos=(30, 0, -500))
rend3.glRender()
rend3.glFinish("newVertexAndColorScale.bmp")

