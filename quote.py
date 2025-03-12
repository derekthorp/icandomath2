from manim import *

class QuoteAnimation(Scene):
    def construct(self):
        # Create the quote text split across two lines
        quote_line1 = Text("\"A discovery is said to be an accident", 
                          font_size=36, color=GOLD_B)
        quote_line2 = Text("meeting a prepared mind\"", 
                          font_size=36, color=GOLD_B)
        
        # Arrange the lines vertically
        quote_group = VGroup(quote_line1, quote_line2)
        quote_group.arrange(DOWN, buff=0.3)
        quote_group.move_to(ORIGIN)
        
        # Create the author text
        author = Text("- Albert Szent-Györgyi", 
                     font_size=20, color=GOLD_A)
        author.next_to(quote_group, DOWN, buff=0.7)
        
        # Fade in the quote and author
        self.play(FadeIn(quote_line1), FadeIn(quote_line2), FadeIn(author))
        
        # Wait for 5 seconds
        self.wait(3)
        
        # Fade out the quote and author
        self.play(FadeOut(quote_line1), FadeOut(quote_line2), FadeOut(author))
        
        # Wait a moment before ending
        self.wait(1)

# To run this animation:
# manim -pql quote_animation.py QuoteAnimation