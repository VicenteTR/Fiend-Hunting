import math

class Exiva:
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_max = 0
        self.x_min = 0
        self.y_max = 0
        self.y_min = 0
        self.distance_ranges = {
            "Nearby": (0, 4),
            "Normal": (5, 100),
            "Far": (101, 250),
            "Very Far": (251, 2500)
        }
        self.directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    
    
    def get_vertices(self, direction, ran):
       vertices = {"S": {
            "Nearby": [(4,4),(-4,4),(-4,-4),(4,-4)],
            "Normal": [(4*(math.sqrt(2)-1), 4),(-4*(math.sqrt(2)-1),4),(-100*(math.sqrt(2)-1),100),(100*(math.sqrt(2)-1),100)],
            "Far": [(100*(math.sqrt(2)-1), 100),(-100*(math.sqrt(2)-1),100),(-250*(math.sqrt(2)-1),250),(250*(math.sqrt(2)-1),250)],
            "Very Far": [(250*(math.sqrt(2)-1), 250),(-250*(math.sqrt(2)-1),250),(-2500*(math.sqrt(2)-1),2500),(2500*(math.sqrt(2)-1),2500)]
        },
        "SE": {
            "Nearby": [(4,4),(-4,4),(-4,-4),(4,-4)],
            "Normal": [(4,4*(math.sqrt(2)-1)),(4,4),(4*(math.sqrt(2)-1), 4),(100*(math.sqrt(2)-1),100),(100, 100),(100,100*(math.sqrt(2)-1))],
            "Far": [(100,100*(math.sqrt(2)-1)),(100,100),(100*(math.sqrt(2)-1), 100),(250*(math.sqrt(2)-1),250),(250, 250),(250,250*(math.sqrt(2)-1))],
            "Very Far": [(250,250*(math.sqrt(2)-1)),(250,250),(250*(math.sqrt(2)-1), 250),(2500*(math.sqrt(2)-1),2500),(2500, 2500),(2500,2500*(math.sqrt(2)-1))]
        },
        "E": {
            "Nearby": [(4,4),(-4,4),(-4,-4),(4,-4)],
            "Normal": [(4,4*(math.sqrt(2)-1)),(4,-4*(math.sqrt(2)-1)),(100,-100*(math.sqrt(2)-1)),(100, 100*(math.sqrt(2)-1))],
            "Far": [(100,100*(math.sqrt(2)-1)),(100,-100*(math.sqrt(2)-1)),(250,-250*(math.sqrt(2)-1)),(250, 250*(math.sqrt(2)-1))],
            "Very Far": [(250,250*(math.sqrt(2)-1)),(250,-250*(math.sqrt(2)-1)),(2500,-2500*(math.sqrt(2)-1)),(2500, 2500*(math.sqrt(2)-1))]
        },
        "NE": {
            "Nearby": [(4,4),(-4,4),(-4,-4),(4,-4)],
            "Normal": [(4,-4*(math.sqrt(2)-1)),(4,-4),(4*(math.sqrt(2)-1),-4),(100*(math.sqrt(2)-1), -100),(100,-100),(100, -100*(math.sqrt(2)-1))],
            "Far": [(100,-100*(math.sqrt(2)-1)),(100,-100),(100*(math.sqrt(2)-1),-100),(250*(math.sqrt(2)-1), -250),(250,-250),(250, -250*(math.sqrt(2)-1))],
            "Very Far": [(250,-250*(math.sqrt(2)-1)),(250,-250),(250*(math.sqrt(2)-1),-250),(2500*(math.sqrt(2)-1), -2500),(2500,-2500),(2500, -2500*(math.sqrt(2)-1))]
        },
        "N": {
            "Nearby": [(4,4),(-4,4),(-4,-4),(4,-4)],
            "Normal": [(4*(math.sqrt(2)-1), -4),(-4*(math.sqrt(2)-1),-4),(-100*(math.sqrt(2)-1),-100),(100*(math.sqrt(2)-1),-100)],
            "Far": [(100*(math.sqrt(2)-1), -100),(-100*(math.sqrt(2)-1),-100),(-250*(math.sqrt(2)-1),-250),(250*(math.sqrt(2)-1),-250)],
            "Very Far": [(250*(math.sqrt(2)-1), -250),(-250*(math.sqrt(2)-1),-250),(-2500*(math.sqrt(2)-1),-2500),(2500*(math.sqrt(2)-1),-2500)]
        },
        "NW": {
            "Nearby": [(4,4),(-4,4),(-4,-4),(4,-4)],
            "Normal": [(-4,-4*(math.sqrt(2)-1)),(-4,-4),(-4*(math.sqrt(2)-1), -4),(-100*(math.sqrt(2)-1),-100),(-100,-100),(-100,-100*(math.sqrt(2)-1))],
            "Far": [(-100,-100*(math.sqrt(2)-1)),(-100,-100),(-100*(math.sqrt(2)-1), -100),(-250*(math.sqrt(2)-1),-250),(-250,-250),(-250,-250*(math.sqrt(2)-1))],
            "Very Far": [(-250,-250*(math.sqrt(2)-1)),(-250,-250),(-250*(math.sqrt(2)-1), -250),(-2500*(math.sqrt(2)-1),-2500),(-2500,-2500),(-2500,-2500*(math.sqrt(2)-1))]
        },
        "W": {
            "Nearby": [(4,4),(-4,4),(-4,-4),(4,-4)],
            "Normal": [(-4,4*(math.sqrt(2)-1)),(-4,-4*(math.sqrt(2)-1)),(-100,-100*(math.sqrt(2)-1)),(-100, 100*(math.sqrt(2)-1))],
            "Far": [(-100,100*(math.sqrt(2)-1)),(-100,-100*(math.sqrt(2)-1)),(-250,-250*(math.sqrt(2)-1)),(-250, 250*(math.sqrt(2)-1))],
            "Very Far": [(-250,250*(math.sqrt(2)-1)),(-250,-250*(math.sqrt(2)-1)),(-2500,-2500*(math.sqrt(2)-1)),(-2500, 2500*(math.sqrt(2)-1))]
        },
        "SW": {
            "Nearby": [(4,4),(-4,4),(-4,-4),(4,-4)],
            "Normal": [(-4,4*(math.sqrt(2)-1)),(-4,4),(-4*(math.sqrt(2)-1),4),(-100*(math.sqrt(2)-1), 100),(-100,100),(-100, 100*(math.sqrt(2)-1))],
            "Far": [(-100,100*(math.sqrt(2)-1)),(-100,100),(-100*(math.sqrt(2)-1),100),(-250*(math.sqrt(2)-1), 250),(-250,250),(-250, 250*(math.sqrt(2)-1))],
            "Very Far": [(-250,250*(math.sqrt(2)-1)),(-250,250),(-250*(math.sqrt(2)-1),250),(-2500*(math.sqrt(2)-1), 2500),(-2500,2500),(-2500, 2500*(math.sqrt(2)-1))]
        },
        " ": {
            "Nearby": [(4,4),(-4,4),(-4,-4),(4,-4)]
        }}
       
       return vertices[direction][ran]
    
    def calculate_distance(self, range_key, direction):
        min_distance, max_distance = self.distance_ranges[range_key]
        if direction == "N":
            self.x_max = self.x_pos + max_distance
            self.x_min = self.x_pos - max_distance
            self.y_max = self.y_pos - max_distance
            self.y_min = self.y_pos - min_distance
        elif direction == "NE":
            self.x_max = self.x_pos + max_distance
            self.x_min = self.x_pos + min_distance
            self.y_max = self.y_pos - max_distance
            self.y_min = self.y_pos - min_distance
        elif direction == "E":
            self.x_max = self.x_pos + max_distance
            self.x_min = self.x_pos + min_distance
            self.y_max = self.y_pos + max_distance
            self.y_min = self.y_pos - max_distance
        elif direction == "SE":
            self.x_max = self.x_pos + max_distance
            self.x_min = self.x_pos + min_distance
            self.y_max = self.y_pos + max_distance
            self.y_min = self.y_pos + min_distance
        elif direction == "S":
            self.x_max = self.x_pos + max_distance
            self.x_min = self.x_pos - max_distance
            self.y_max = self.y_pos + max_distance
            self.y_min = self.y_pos + min_distance
        elif direction == "SW":
            self.x_max = self.x_pos - max_distance
            self.x_min = self.x_pos - min_distance
            self.y_max = self.y_pos + max_distance
            self.y_min = self.y_pos + min_distance
        elif direction == "W":
            self.x_max = self.x_pos - max_distance
            self.x_min = self.x_pos - min_distance
            self.y_max = self.y_pos - max_distance
            self.y_min = self.y_pos + max_distance
        elif direction == "NW":
            self.x_max = self.x_pos - max_distance
            self.x_min = self.x_pos - min_distance
            self.y_max = self.y_pos - max_distance
            self.y_min = self.y_pos - min_distance
        
    def print_all(self):
        print("X ranges: (", self.x_min, ",", self.x_max, " )")
        print("Y ranges: (", self.y_min, ",", self.y_max, " )")


#exiva = Exiva(0, 0)
#vertices = exiva.get_vertices("NE", "Normal")
#print(vertices)
