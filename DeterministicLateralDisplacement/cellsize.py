from manim import *

class RedBloodCellPulsation(Scene):
    def construct(self):
        # Import the SVG file
        rbc = SVGMobject("rbc.svg")
        
        # Set initial color and position
        rbc.scale(.75)  # Initial scale
        rbc.move_to(LEFT * 3)  # Center of the screen
        
        # Add the red blood cell to the scene
        self.play(FadeIn(rbc))

        self.wait(3)
        
        # Create the pulsation animation (scaling up and down)
        # We'll do 3 cycles of pulsation
        for _ in range(2):
            # Scale up
            self.play(
                rbc.animate.scale(3),  # Scale up by 1.5x
                run_time=1
            )

            self.wait(1)
            
            # Scale down
            self.play(
                rbc.animate.scale(1/3),  # Scale back down
                run_time=1
            )

            self.wait(1)

        self.wait(4)
        
        # Fade out at the end
        self.play(FadeOut(rbc))


# To run this animation, use the following command in your terminal:
# manim -pql redbloodcell_animation.py RedBloodCellPulsation
