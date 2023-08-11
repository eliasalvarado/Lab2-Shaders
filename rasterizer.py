from gl import Renderer
import shaders


width = 500
height = 500

rend = Renderer(width, height)
rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.flatShader

scaleDim = 100

#Medium shot
rend.glLoadModel(filename = "model.obj",
                texName = "model.bmp",
                translate=(0, 0, -500),
                rotate=(0, 0, 0),
                scale=(scaleDim, scaleDim, scaleDim))

""" rend.glLookAt(camPos=(0, 50, 0),
                eyePos=(0, 0, -500)) """

rend.glRender()

rend.glFinish("output.bmp")

