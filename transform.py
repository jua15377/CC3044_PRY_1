from glm import *


def transform(v1, viewPort, move,rotation, axis, rescale, camara, where_to_look):
    vertex = vec3(*v1)
    vertex = vec4(vertex, 1)
    i = mat4(1)
    translateM = translate(i, vec3(move[0], move[1], move[2]))
    if (axis == "x"):
        rotationM = rotate(i, radians(rotation), (1, 0, 0))
    if (axis == "y"):
        rotationM = rotate(i, radians(rotation), (0, 1, 0))
    if (axis == "z"):
        rotationM = rotate(i, radians(rotation), (0, 0, 1))
    scaleM = scale(i, (rescale[0], rescale[1], rescale[2]))
    modelM = translateM * rotationM * scaleM
    # camara
    viewM = lookAt(vec3(camara[0], camara[1], camara[2]), vec3(*where_to_look), vec3(0, 1, 0))
    projectM = mat4(
        1, 0, 0, 0,
        0, 1, 0, 0,
        0, 0, 1, -0.001,
        0, 0, 0, 1
    )

    viewPortM = mat4(
        1, 0, 0, 0,
        0, 1, 0, 0,
        0, 0, 1, 0,
        viewPort.width/2, viewPort.height/2, 128, 1
    )
    vertex = viewPortM * projectM * viewM * modelM * vertex
    vertex = vec3(vertex/vertex.w)
    # print(vertex)
    return vertex