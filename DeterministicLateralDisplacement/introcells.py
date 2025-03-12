from manim import *
import numpy as np
import os

class BloodCellScene(Scene):
    def construct(self):
        # Create cell objects (shape and label pairs)
        cells = {
            "rbc": {"shape": None, "label": Text("Red Blood Cell").scale(0.5)},
            "wbc": {"shape": None, "label": Text("White Blood Cell").scale(0.5)},
            "ctc": {"shape": None, "label": Text("Circulating Tumor Cell").scale(0.5)},
            "platelet": {"shape": None, "label": Text("Platelet").scale(0.5)}
        }
        
        # Try to load SVGs, or create fallback shapes
        for name in cells:
            svg_path = f"{name}.svg"
            try:
                if os.path.exists(svg_path):
                    shape = SVGMobject(svg_path)
                    # Set scale factors for different cell types
                    if name == "wbc":
                        # Make white blood cell larger (1.7x scale factor)
                        shape = shape.scale(1.9)
                        # Try to set fill color to white for all submobjects
                        for submob in shape.submobjects:
                            try:
                                submob.set_fill(WHITE, opacity=1)
                                submob.set_stroke(WHITE, width=2)
                            except:
                                pass
                    elif name == "platelet":
                        # Make platelet smaller (0.7x scale factor)
                        shape = shape.scale(0.7)
                    # For CTC, try to make it more visible
                    elif name == "ctc":
                        shape = shape.scale(1.2)
                    if name == "ctc":
                        # Check if CTC has visible submobjects
                        if len(shape.submobjects) == 0:
                            print("Warning: CTC SVG has no submobjects, using fallback")
                            shape = self.create_fallback_shape(name)
                        else:
                            print(f"CTC SVG loaded with {len(shape.submobjects)} submobjects")
                            # Try to set a default color if needed
                            for submob in shape.submobjects:
                                try:
                                    # Only set color if it's not already set
                                    if submob.get_fill_opacity() < 0.1:
                                        submob.set_fill(PURPLE, opacity=0.8)
                                    if submob.get_stroke_width() < 0.1:
                                        submob.set_stroke(PURPLE_A, width=1.5)
                                except:
                                    pass
                    cells[name]["shape"] = shape.scale(0.8)
                else:
                    cells[name]["shape"] = self.create_fallback_shape(name)
            except Exception as e:
                print(f"Error creating {name}: {e}")
                cells[name]["shape"] = self.create_fallback_shape(name)  # Simple fallback
        
        # Create groups with shapes and labels, ensuring consistent spacing
        groups = []
        for name, parts in cells.items():
            if parts["shape"] is not None:
                # Create a container to hold both shape and label with fixed spacing
                container = VGroup()
                shape = parts["shape"]
                label = parts["label"]
                
                # Add shape and label to container with consistent arrangement
                container.add(shape)
                container.add(label)
                
                # Arrange vertically with consistent buffer
                container.arrange(DOWN, buff=0.3)
                
                groups.append(container)
        
        # Arrange all groups horizontally with less space
        all_groups = VGroup(*groups).arrange(RIGHT, buff=1.2)
        all_groups.center()
        
        # Add "not to scale" label at bottom center
        scale_label = Text("*NOT TO SCALE").scale(0.45)
        scale_label.to_edge(DOWN, buff=.85)
        
        # Add all mobjects to the scene
        self.add(all_groups, scale_label)
        self.wait(1)  # Wait 1 second before starting rotations
        
        # Set rotation speeds (radians per frame at 60fps)
        speeds = {
            "rbc": 0.05,
            "wbc": 0.007,
            "ctc": 0.013,
            "platelet": 0.009
        }
        
        # Reduced number of frames - 300 frames (5 seconds at 60fps)
        frames = 900
        for i in range(frames):
            anims = []
            
            # Rotate each cell shape
            for j, group in enumerate(groups):
                name = list(cells.keys())[j]
                if len(group) >= 1 and group[0] is not None:  # Shape is the first element
                    angle = speeds[name]
                    # Create a simple rotation transformation
                    anims.append(Rotate(group[0], angle=angle, about_point=group[0].get_center()))
            
            # Play one frame of animation
            if anims:
                self.play(*anims, run_time=1/60)
        
        # Fade out everything at the end
        self.play(FadeOut(all_groups), FadeOut(scale_label), run_time=1)
    
    def create_fallback_shape(self, cell_type):
        """Creates a simple shape based on cell type"""
        if cell_type == "rbc":
            return Circle(radius=0.6)  # Simple circle for red blood cell
        elif cell_type == "wbc":
            return Circle(radius=0.7)  # Larger circle for white blood cell
        elif cell_type == "ctc":
            # Green parallelogram for CTC with height = half of width
            width = 1.2
            height = width / 2  # Height is half of width
            skew = 0.2
            
            parallelogram = Polygon(
                [-width/2, -height/2, 0],
                [width/2, -height/2, 0],
                [width/2 - skew, height/2, 0],
                [-width/2 - skew, height/2, 0],
                fill_color=GREEN,
                fill_opacity=0.8,
                stroke_color=GREEN_E,  # Dark green border
                stroke_width=3  # Thicker border for emphasis
            )
            return parallelogram
        else:  # platelet
            return Ellipse(width=0.8, height=0.5)  # Oval for platelet


# To run this animation, use:
# manim -pql blood_cells.py BloodCellScene
# 
# Note: This uses -pql (low quality) for faster rendering during development
# For final version, use -pqh (high quality)
