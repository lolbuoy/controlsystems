import math

def distance_and_angle(x1, y1, x2, y2):
    # Calculate the distance between the two points
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    # Calculate the angle between the two points
    angle = math.atan2(y2 - y1, x2 - x1)
    angle_degrees = math.degrees(angle)

    return distance, angle_degrees

# Example usage
x1, y1 = 1, 1
x2, y2 = 4, 5

distance, angle = distance_and_angle(x1, y1, x2, y2)

print("Distance between the two points:", distance)
print("Angle between the two points (in degrees):", angle)

point1 = (100, 200)
point2 = (500, 600)

# calculate the distance between the two points in pixels
pixel_distance = math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

# calculate the angle between the two points in radians
angle = math.atan2(point2[1] - point1[1], point2[0] - point1[0])

# convert the pixel distance to real-life distance using the GSD constant
#real_distance = pixel_distance * gsd

print("Pixel distance:", pixel_distance)
print("Angle:", math.degrees(angle))
#print("Real-life distance:", real_distance)
