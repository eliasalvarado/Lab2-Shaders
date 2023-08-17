from gl import Renderer, Model
import shaders


width = 500
height = 500

rend = Renderer(width, height)
rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.multiTextureShader

scaleDim = 10

""" rend.glLoadModel(filename = "model.obj",
                texNames = ["model.bmp"],
                translate=(0, 0, -500),
                rotate=(0, 0, 0),
                scale=(scaleDim, scaleDim, scaleDim)) """

rend.glLoadModel(filename = "sword.obj",
                texNames = ["swordtex.bmp", "swordtex1.bmp"],
                translate=(0, 100, -500),
                rotate=(95, 50, 0),
                scale=(scaleDim, scaleDim, scaleDim))

rend.glLookAt(camPos=(0, 0, 0),
                eyePos=(30, 0, -500))

rend.glRender()

rend.glFinish("output.bmp")

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

rend1.glFinish("output1.bmp")

rend1 = Renderer(width, height)

rend1.vertexShader = shaders.vertexShader
rend1.fragmentShader = shaders.neonShader

rend1.glLoadModel(filename = "sword.obj",
                texNames = ["swordtex.bmp", "swordtex1.bmp"],
                translate=(0, 100, -500),
                rotate=(95, 50, 0),
                scale=(scaleDim, scaleDim, scaleDim))

rend1.glLookAt(camPos=(0, 0, 0),
                eyePos=(30, 0, -500))

rend1.glRender()

rend1.glFinish("output2.bmp")

