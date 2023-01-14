import numpy as np

def parse_stl_vertices(filename):
    # Open the STL file and read its contents into a list of lines
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Initialize an empty list to store the vertex coordinates
    vertices = []

    # Iterate over the lines in the file
    for line in lines:
        # Split the line into words
        words = line.split()
        # Check if the first word is 'vertex' (which indicates a vertex coordinate)
        if len(words) > 0 and words[0] == 'vertex':
            # Parse the coordinates from the line and add them to the list
            vertex = [float(words[i]) for i in range(1, 4)]
            vertices.append(vertex)

    # Convert the list of vertices to a NumPy array and return it
    return np.array(vertices)

def move_verticies(verticies, rake, CoR, yMorphRange):
    # CoR is the x-coord for the center of rotation. 
    # yMorphRange describes the y coords for the inner and outer pickup points. for example (0.05, 0.55) 
    # Returns an array with the moved verticies. 
    yMorphRange = np.sort(yMorphRange)
    new_verticies = []

    for vertex in verticies:
        dist = vertex[0]-CoR # X-Distance from the center of rotation to the vertex of interest. 

        maxVerticalDist = dist*np.sin(np.radians(rake)) # Maxium vertical deformation for this X-distance. 

        if (abs(vertex[1]) < max(yMorphRange)) and (abs(vertex[1]) > min(yMorphRange)): # Checks if the y coord is within the morphrange 

            verticalDist = np.interp(abs(vertex[1]), yMorphRange, [maxVerticalDist, 0])
            vertex[2] = vertex[2]+verticalDist
        elif abs(vertex[1]) < min(yMorphRange):
            vertex[2] = vertex[2]+maxVerticalDist

        new_verticies.append(vertex)

    return new_verticies

def write_stl(vertices, filename):
    solidname = filename[::-1]
    solidname = solidname[3:solidname.find("/")]
    solidname = solidname[::-1]
    with open(filename, "w") as f:
        f.write("solid object " + solidname + "\n")
        for i in range(0, len(vertices), 3):
            v1, v2, v3 = vertices[i:i+3]
            # Calculate the facet normal
            v1 = np.array(v1)
            v2 = np.array(v2)
            v3 = np.array(v3)
            normal = np.cross(v2 - v1, v3 - v1)
            normal /= np.linalg.norm(normal)
            f.write("   facet normal {:.6E} {:.6E} {:.6E}\n".format(normal[0], normal[1], normal[2]))
            f.write("      outer loop\n")
            f.write("         vertex {:.6E} {:.6E} {:.6E}\n".format(v1[0], v1[1], v1[2]))
            f.write("         vertex {:.6E} {:.6E} {:.6E}\n".format(v2[0], v2[1], v2[2]))
            f.write("         vertex {:.6E} {:.6E} {:.6E}\n".format(v3[0], v3[1], v3[2]))
            f.write("      endloop\n")
            f.write("   endfacet\n")
        f.write("endsolid object\n")

def morph_suspension(input_file, output_file, rake, CoR, morphRange):
    nonMorphVerticies = parse_stl_vertices(input_file)
    morphedVerticies = move_verticies(nonMorphVerticies, rake, CoR, morphRange)
    write_stl(morphedVerticies, output_file)

# Example below

front = "<-- some path --> /MAND_Susp_frt_V02.stl"
rear = "<-- some path --> /MAND_Susp_rr_V02.stl"

rearMorphed = "<-- some path --> /MAND_Susp_rr_V02_MORPHED.stl"
frontMorphed = "<-- some path --> /MAND_Susp_frt_V02_MORPHED.stl"

frontYMorphRange = (0.125, 0.64)
rearYMorphRange = (0.05, 0.55)
rake = 3 # positive rake angle is nose up 
CoR = 0.43 # Front edge of the plank

morph_suspension(front, frontMorphed, rake, CoR, frontYMorphRange)
morph_suspension(rear, rearMorphed, rake, CoR, rearYMorphRange)






