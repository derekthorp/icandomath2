from manim import *

class CreditsScene(Scene):
    def construct(self):
        # Create the title text
        title = Text("Special Thanks!", font_size=36, color=WHITE)
        title.to_edge(UP, buff=1)
        
        # Create the reference texts individually with manual positioning
        references = [
            "Huang, L. R., Cox, E. C., Austin, R. H., & Sturm, J. C. (2004). Continuous particle separation",
            "through deterministic lateral displacement. Science (New York, N.Y.), 304(5673), 987–990.",
            "https://doi.org/10.1126/science.1094567",
            "",
            "Hochstetter, A., Vernekar, R., Austin, R. H., Becker, H., Beech, J. P., Fedosov, D. A., ... & Inglis, D. W. (2020).",
            "Deterministic lateral displacement: Challenges and perspectives. ACS nano, 14(9), 10784-10795.",
            "",
            "Timm Krüger – Lattice Boltzmann Computational Fluid Dynamics (CFD) Model, YouTube (2015)",
            "",
            "Lotto Maniac – Stake Plinko, YouTube (2024)",
            "",
            "NIH Bioart",
            "",
            "Claude Sonnet 3.7, My Loving and Supportive Code Assist"
        ]
        
        # Create text objects individually
        ref_texts = []
        current_y = title.get_bottom()[1] - 0.7  # Start below title with space
        
        for line in references:
            # Skip empty lines with extra space
            if line == "":
                current_y -= 0.3
                continue
                
            ref_line = Text(line, font_size=18, color=GREY)
            # Position each line manually
            ref_line.move_to([0, current_y, 0])
            current_y -= 0.35  # Move down for next line
            ref_texts.append(ref_line)
        
        # Group all reference text objects for animation
        reference_group = VGroup(*ref_texts)
        
        # Center the reference group horizontally
        for text in ref_texts:
            text.set_x(0)  # Center each text on the x-axis
        
        # Animation sequence
        # 1. Fade in title
        self.play(FadeIn(title), run_time=1)
        
        # 2. Fade in all references
        self.play(*[FadeIn(text) for text in ref_texts], run_time=1.5)
        
        # 3. Hold on screen for viewing
        self.wait(2)
        
        # 4. Fade everything out
        self.play(
            FadeOut(title),
            *[FadeOut(text) for text in ref_texts],
            run_time=2
        )
        
        # Final pause
        self.wait(1)


# To run this animation:
# manim -pql credits.py CreditsScene