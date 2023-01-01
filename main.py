
# ------------------------------------------------------ imports ------------------------------------------------------ #

import pygame
import math
import rich

pygame.font.init()
font = pygame.font.SysFont("comicsans", 15)

# ------------------------------------------------------ constants ---------------------------------------------------- #

width = 500
height = 500
MAX_WEIGHT = 100

display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Kruskal's algorithm")

# ------------------------------------------------------ COLOR ------------------------------------------------------- #

class Color:
    bg = (46, 52, 64)
    light = (216, 222, 233)
    dark = (94, 129, 172)
    edge = (70, 100, 119)

# --------------------------------------------------- UTILS FUNCS ---------------------------------------------------- #

def render_text(txt: str, win: pygame.display, x: int, y: int):
    render_text = font.render(str(txt), True, Color.light)
    win.blit(render_text, (x, y))

# ------------------------------------------------------ VERTEX ------------------------------------------------------ #

class Vertex:
    vertex_index = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.coords = (self.x, self.y)
        self.visited = False
        self.index = Vertex.vertex_index
        self.edges = []

        # increment the class variable "vertex_index"
        Vertex.vertex_index += 1

    def draw(self, win):
        pygame.draw.circle(win, Color.dark, (self.x, self.y), 5)
        render_text = font.render(str(self.index), True, Color.light)
        win.blit(render_text, (self.x, self.y))

# ------------------------------------------------------ EDGE ------------------------------------------------------ #


class Edge:
    def __init__(self, from_: Vertex, to_: Vertex, weight: int):
        self.f = from_
        self.t = to_
        self.w = weight

        self.highlight = False

    def includes(self, vert):
        if self.f.index == vert.index:
            return True

        if self.t.index == vert.index:
            return True 
        
        return False

    def __str__(self):
        return f"{self.f.index} <==> {self.t.index} | {self.w}"

    def dump(self):
        return self.f.index, self.t.index, self.w

    def draw(self, win):
        pygame.draw.line(win, Color.edge, (self.f.x, self.f.y), (self.t.x, self.t.y), 5)

# ---------------------------------------------------- kruskal ---------------------------------------------------- #

def get_accessible_edges(vertex, lookup):
    prev = set()
    curr = set([vertex])

    while prev != curr:
        prev = prev.union(curr)

        for edge in lookup:
            f, t, _ = edge.dump()

            if f in prev and t in prev:
                continue

            elif f in prev:
                curr.add(t)
            
            elif t in prev:
                curr.add(f)

    return curr

def kruskal(edges):
    mst = []
    edges = sorted(edges, key = lambda x: x.w)

    
    for edge in edges:
        f, t, _ = edge.dump()

        if mst == []:
            mst.append(edge)

        else:
            f_accessible = set(get_accessible_edges(f, mst))
            t_accessible = set(get_accessible_edges(t, mst))

            if len(f_accessible.intersection(t_accessible)) == 0:
                mst.append(edge)

    for e in mst:
        e.highlight = True

    return mst

# ----------------------------------------------------- main func ---------------------------------------------------- #

def main():
    run = True
    verts: list[Vertex] = []
    edges: list[Edge] = []
    selected: list[Vertex] = []
    user_weight = ''
    prompted = False

    while run:
        display.fill(Color.bg)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:                                                       # left mouse button          
                    if not prompted:    
                        # vertx creation
                        x, y = pygame.mouse.get_pos()
                        new_vertex = Vertex(x, y)
                        verts.append(new_vertex)
                    else:
                        print("Enter a valid input")

                elif event.button == 3:                                                     # right mouse button
                    if len(verts) >= 2:
                        pos = pygame.mouse.get_pos()
                        short_dist = math.inf
                        nearest_vert = None
                        for vert in verts:
                            point_dist = math.dist(vert.coords, pos)
                            if point_dist < short_dist:
                                short_dist = point_dist
                                nearest_vert = vert

                        selected.append(nearest_vert)

                        if len(selected) >= 2:
                            new_edge = Edge(selected[0], selected[1], MAX_WEIGHT)           # edge creation
                            edges.append(new_edge)
                            selected = []
                            prompted = True                                                 # prompt the user for edge weight after edge creation

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    print([e for e in edges])

                if event.key == pygame.K_RETURN:
                    try:
                        edges[-1].w = int(user_weight)
                    except:
                        user_weight = ''
                        break

                    user_weight = ''
                    prompted = False
                else:
                    # If user is prompted, only then we add the keystrokes to the user_weight variable
                    if prompted:
                        user_weight += pygame.key.name(event.key)

                if event.key == pygame.K_d:
                    if len(verts) != 0:

                        # KRUSKAL
                        mst = kruskal(edges)
                        edges = mst

                    else:
                        rich.print("[bold red]ERROR[/bold red] : [bold blue]No graph found[/bold blue]")

                if event.key == pygame.K_BACKSPACE:
                    user_weight = ''

                if event.key == pygame.K_DELETE:
                    if len(verts) > 0:
                        last_vert = verts[-1]
                        for edge in edges:
                            if edge.includes(last_vert):
                                edges.remove(edge)  
                        verts = verts[:-1]
                        Vertex.vertex_index -= 1
                    else:
                        rich.print("[bold red]ERROR[/bold red] : [bold blue]No vertices to delete[/bold blue]")

        if prompted:
            render_text("Weight: ", display, 0, 10)
            render_text(user_weight, display, 60, 10)

        for edge in edges:
            edge.draw(display)
                
        for vert in verts:
            vert.draw(display)

        for vert in selected:
            pygame.draw.circle(display, Color.light, vert.coords, 7, 1)

        pygame.display.flip()

# --------------------------------------------- calling the main func ------------------------------------------------- #

if __name__ == "__main__":
    main()

# --------------------------------------------------------------------------------------------------------------------- #
