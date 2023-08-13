from gl import Renderer, Model
import shaders


width = 500
height = 500

rend = Renderer(width, height)
rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.heightColorShader

scaleDim = 200

rend.glLoadModel(filename = "model.obj",
                texNames = ["model.bmp"],
                translate=(0, 0, -500),
                rotate=(0, 0, 0),
                scale=(scaleDim, scaleDim, scaleDim))

""" rend.glLoadModel(filename = "sword.obj",
                texNames = ["swordtex.bmp", "swordtex1.bmp"],
                vertexShader = shaders.vertexShader,
                fragmentShader = shaders.multiTextureShader,
                translate=(0, 0, -500),
                rotate=(90, 50, 0),
                scale=(scaleDim, scaleDim, scaleDim)) """

""" rend.glLoadModel(filename = "sword.obj",
                texNames = ["swordtex.bmp", "swordtex1.bmp"],
                translate=(100, 0, -500),
                rotate=(90, 50, 0),
                scale=(scaleDim, scaleDim, scaleDim)) """

rend.glLookAt(camPos=(0, 0, 0),
                eyePos=(30, 0, -500))

rend.glRender()

rend.glFinish("output1.bmp")

