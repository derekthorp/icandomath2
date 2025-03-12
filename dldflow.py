from manim import *
import numpy as np

class DeterministicLateralDisplacement(Scene):
    def construct(self):
        # Configuration
        num_pillars = 10
        pillar_radius = 0.3
        pillar_color = BLUE
        pillar_spacing = 2.5 * pillar_radius  # Space between centers of pillars
        y_position = 2  # Position the array will move to later
        
        # Calculate total width of the pillar array to center it
        total_width = (num_pillars - 1) * pillar_spacing
        start_x = -total_width / 2
        
        # Create a group to hold all pillars
        pillars = VGroup()
        
        # Create the horizontal row of pillars (initially at y=0)
        for i in range(num_pillars):
            x_pos = start_x + i * pillar_spacing
            pillar = Circle(radius=pillar_radius, color=pillar_color, fill_opacity=0.8)
            pillar.move_to([x_pos, 0, 0])  # Start at y=0
            pillars.add(pillar)
        
        # Add title to the scene
        title = Text("Deterministic Lateral Displacement (DLD)", font_size=36)
        title.to_edge(UP, buff=0.5)
        
        # Add the elements to the scene with animations
        self.play(Write(title))
        self.play(Create(pillars))
        self.wait(1)
        
        # Add an annotation
        annotation = Text("Single Row of Micropillars", font_size=24)
        annotation.next_to(pillars, DOWN, buff=0.5)
        self.play(FadeIn(annotation))
        
        # Position the lambda label between the first and second pillars
        first_pillar = pillars[0]
        second_pillar = pillars[1]
        
        # Get the exact centers of the first two pillars
        p1_center = first_pillar.get_center()
        p2_center = second_pillar.get_center()
        
        # Create a double-headed arrow that spans from center to center
        arrow = DoubleArrow(
            start=p1_center,
            end=p2_center,
            buff=0,  # No buffer - the arrow will go from center to center
            color=WHITE,
            tip_length=0.2
        )
        
        # Create a VGroup for the vertical indicator lines
        indicator_lines = VGroup()
        
        # Create vertical indicator lines at each pillar center
        line1 = Line(
            p1_center + UP * pillar_radius * 1.5,
            p1_center + DOWN * pillar_radius * 1.5,
            color=WHITE,
            stroke_width=2
        )
        
        line2 = Line(
            p2_center + UP * pillar_radius * 1.5,
            p2_center + DOWN * pillar_radius * 1.5,
            color=WHITE,
            stroke_width=2
        )
        
        indicator_lines.add(line1, line2)
        
        # Add the lambda label below the arrow
        midpoint = (p1_center + p2_center) / 2
        lambda_label = MathTex(r"\lambda")
        lambda_label.move_to(midpoint + DOWN * 0.5)
        
        # Create and display arrow, indicator lines, and label
        self.play(Create(arrow), Create(indicator_lines), Write(lambda_label))
        
        self.wait(1)
        
        # Store original positions for later
        original_positions = [pillar.get_center() for pillar in pillars]
        
        # Calculate new positions with increased spacing
        increased_spacing = pillar_spacing * 1.75  # Increment the spacing
        new_total_width = (num_pillars - 1) * increased_spacing
        new_start_x = -new_total_width / 2
        
        # Define animations for each pillar to move to its new position
        expand_anims = []
        for i, pillar in enumerate(pillars):
            new_x = new_start_x + i * increased_spacing
            expand_anims.append(pillar.animate.move_to([new_x, 0, 0]))  # Keep at y=0
        
        # Create separate updaters for each element to ensure proper updating
        
        # Arrow updater
        def arrow_updater(arrow):
            start = pillars[0].get_center()
            end = pillars[1].get_center()
            arrow.put_start_and_end_on(start, end)
            return arrow
            
        # Line updaters
        def line1_updater(line):
            center = pillars[0].get_center()
            line.put_start_and_end_on(
                center + UP * pillar_radius * 1.5,
                center + DOWN * pillar_radius * 1.5
            )
            return line
            
        def line2_updater(line):
            center = pillars[1].get_center()
            line.put_start_and_end_on(
                center + UP * pillar_radius * 1.5,
                center + DOWN * pillar_radius * 1.5
            )
            return line
            
        # Lambda label updater
        def lambda_updater(label):
            new_midpoint = (pillars[0].get_center() + pillars[1].get_center()) / 2
            label.move_to(new_midpoint + DOWN * 0.5)
            return label
        
        # Add the updaters
        arrow.add_updater(arrow_updater)
        line1.add_updater(line1_updater)
        line2.add_updater(line2_updater)
        lambda_label.add_updater(lambda_updater)
        
        # Animate the expansion of pillars
        self.play(*expand_anims, run_time=2)
        self.wait(1)
        
        # Animate decreasing back to original positions
        contract_anims = []
        for i, pillar in enumerate(pillars):
            contract_anims.append(pillar.animate.move_to(original_positions[i]))
        
        # Animate the contraction of the pillars
        self.play(*contract_anims, run_time=2)
        
        # Add a final scaling of 1.75x pillar_spacing
        final_spacing = pillar_spacing * 1.75
        final_total_width = (num_pillars - 1) * final_spacing
        final_start_x = -final_total_width / 2
        
        # Define animations for final pillar spacing (still at y=0)
        final_anims = []
        for i, pillar in enumerate(pillars):
            final_x = final_start_x + i * final_spacing
            final_anims.append(pillar.animate.move_to([final_x, 0, 0]))  # Keep at y=0
        
        # Animate the final spacing adjustment
        self.play(*final_anims, run_time=2)
        
        # Wait half a second
        self.wait(0.5)
        
        # Fade out only the annotation, keep arrow and lambda
        self.play(FadeOut(annotation))
        
        self.wait(1)
        
        # Remove updaters before moving up
        arrow.remove_updater(arrow_updater)
        line1.remove_updater(line1_updater)
        line2.remove_updater(line2_updater)
        lambda_label.remove_updater(lambda_updater)
        
        # NOW move the pillars upward, along with the arrow, indicator lines, and lambda label
        move_up_anims = [
            pillars.animate.shift(UP * y_position),
            arrow.animate.shift(UP * y_position),
            line1.animate.shift(UP * y_position),
            line2.animate.shift(UP * y_position),
            lambda_label.animate.shift(UP * y_position)
        ]
        self.play(*move_up_anims, run_time=1.5)
        
        self.wait(1)
        
        # Create a full array by adding 4 more rows (for a total of 5)
        num_rows = 5  # Total rows (including the existing one)
        
        # Ensure vertical spacing matches the final horizontal spacing
        vertical_spacing = final_spacing  # Use the same spacing vertically as horizontally
        
        # Create a group to hold all pillar rows
        all_pillar_rows = []  # Store each row separately for later shifting
        all_pillar_rows.append(pillars)  # Add the first row
        
        # Create and add the remaining 4 rows
        for row in range(1, num_rows):
            # Create a new row
            new_row = VGroup()
            
            # Calculate y position for this row
            row_y = y_position - (row * vertical_spacing)
            
            # Copy the pillar pattern from the first row (no shift initially)
            for i in range(num_pillars):
                # Get x position from corresponding pillar in first row
                x_pos = pillars[i].get_center()[0]
                
                # Create a new pillar
                new_pillar = Circle(radius=pillar_radius, color=pillar_color, fill_opacity=0.8)
                new_pillar.move_to([x_pos, row_y, 0])
                new_row.add(new_pillar)
            
            # Add animation to reveal the new row
            self.play(Create(new_row), run_time=0.7)
            
            # Add this row to the collection of rows
            all_pillar_rows.append(new_row)
        
        # Keep the array visible for a moment
        self.wait(2)
        
        # Add a vertical lambda indicator between rows
        # Get positions from the first and second rows
        first_row_pillar = all_pillar_rows[0][0]  # First pillar of first row
        second_row_pillar = all_pillar_rows[1][0]  # First pillar of second row

        # Get the exact centers
        p1_center_v = first_row_pillar.get_center()
        p2_center_v = second_row_pillar.get_center()

        # Create horizontal indicator lines at each row
        h_line1 = Line(
            [p1_center_v[0] - pillar_radius * 1.5, p1_center_v[1], 0],
            [p1_center_v[0] + pillar_radius * 1.5, p1_center_v[1], 0],
            color=WHITE,
            stroke_width=2
        )

        h_line2 = Line(
            [p2_center_v[0] - pillar_radius * 1.5, p2_center_v[1], 0],
            [p2_center_v[0] + pillar_radius * 1.5, p2_center_v[1], 0],
            color=WHITE,
            stroke_width=2
        )

        # Create a vertical double-headed arrow
        v_arrow = DoubleArrow(
            start=[p1_center_v[0] - pillar_radius * 2, p1_center_v[1], 0],
            end=[p1_center_v[0] - pillar_radius * 2, p2_center_v[1], 0],
            buff=0,
            color=WHITE,
            tip_length=0.2
        )

        # Add the vertical lambda label
        v_midpoint = [p1_center_v[0] - pillar_radius * 2.5, (p1_center_v[1] + p2_center_v[1]) / 2, 0]
        v_lambda_label = MathTex(r"\lambda")
        v_lambda_label.move_to(v_midpoint)

        # Create and display the vertical lambda indicator
        self.play(Create(v_arrow), Create(h_line1), Create(h_line2), Write(v_lambda_label))
        self.wait(1)

        # Create a temporary group containing all pillar rows for the flow visualization
        temp_array = VGroup()
        for row in all_pillar_rows:
            temp_array.add(row)
        
        # Create curved streamlines that move around the pillars
        curved_streamlines = self.create_curved_streamlines(temp_array, num_flow_lines=15)
        
        # Fade in the curved streamlines
        self.play(FadeIn(curved_streamlines), run_time=1.5)
        
        # Now add a set of curved flow animations
        # Create particles for the curved streamlines
        particle_streamline_pairs = self.create_particles_on_streamlines(curved_streamlines)
        curved_particles = VGroup()
        for particle, _ in particle_streamline_pairs:
            curved_particles.add(particle)
        
        # Add the particles to the scene
        self.play(FadeIn(curved_particles), run_time=0.5)
        
        # Create animations for the particles following curved paths
        particle_anims = []
        
        for particle, streamline in particle_streamline_pairs:
            # Move the particle along the streamline
            particle_anims.append(
                MoveAlongPath(
                    particle,
                    streamline,
                    run_time=4
                )
            )
        
        # Play all particle animations together
        self.play(*particle_anims)
        
        self.wait(1)
        
        # Clean up the flow visualization before row shifting
        self.play(
            FadeOut(curved_streamlines),
            FadeOut(curved_particles)
        )
        
        # Keep all lambda indicators visible - don't fade them out yet
        
        # Now add an animation to shift the rows (except the first row)
        shift_animations = []
        
        for row_index in range(1, num_rows):
            # Calculate shift amount for this row: row_index * lambda/5
            shift_amount = row_index * (final_spacing / 5)
            
            # Create animation to shift this row to the right
            row_shift = all_pillar_rows[row_index].animate.shift(RIGHT * shift_amount)
            shift_animations.append(row_shift)
        
        # Play the shifting animation
        self.play(
            *shift_animations,
            run_time=2
        )
        
        # Create a group containing all rows
        entire_array = VGroup()
        for row in all_pillar_rows:
            entire_array.add(row)
        
        # Amount to shift left
        left_shift_amount = .5
        
        # Animate the leftward shift - include the horizontal lambda indicators
        self.play(
            entire_array.animate.shift(LEFT * left_shift_amount),
            arrow.animate.shift(LEFT * left_shift_amount),
            line1.animate.shift(LEFT * left_shift_amount),
            line2.animate.shift(LEFT * left_shift_amount),
            lambda_label.animate.shift(LEFT * left_shift_amount),
            run_time=1.5
        )
        
        self.wait(2)
        
        # Add an indicator for delta lambda on the second row
        # First, calculate where the first pillar of the second row would be without shift
        # The shift amount for row 1 (index 1) was: row_index * (final_spacing / 5) = 1 * (final_spacing / 5)
        delta_shift_amount = 1 * (final_spacing / 5)

        # Get the center of the first pillar in second row
        second_row_first_pillar = all_pillar_rows[1][0]
        p2_center_delta = second_row_first_pillar.get_center()

        # Calculate position without shift
        p2_no_shift = [p2_center_delta[0] - delta_shift_amount, p2_center_delta[1], 0]

        # Create vertical indicator lines
        v_line1_delta = Line(
            [p2_no_shift[0], p2_no_shift[1] + pillar_radius * 1.5, 0],
            [p2_no_shift[0], p2_no_shift[1] - pillar_radius * 1.5, 0],
            color=WHITE,
            stroke_width=2
        )

        v_line2_delta = Line(
            [p2_center_delta[0], p2_center_delta[1] + pillar_radius * 1.5, 0],
            [p2_center_delta[0], p2_center_delta[1] - pillar_radius * 1.5, 0],
            color=WHITE,
            stroke_width=2
        )

        # Create a horizontal double-headed arrow
        h_delta_arrow = DoubleArrow(
            start=p2_no_shift,
            end=p2_center_delta,
            buff=0,
            color=WHITE,
            tip_length=0.2
        )

        # Add the delta lambda label
        h_midpoint = [(p2_no_shift[0] + p2_center_delta[0]) / 2, p2_center_delta[1], 0]
        delta_lambda_label = MathTex(r"\Delta\lambda")
        delta_lambda_label.move_to(h_midpoint + DOWN * 0.5)

        # Create and display the delta lambda indicator
        self.play(Create(h_delta_arrow), Create(v_line1_delta), Create(v_line2_delta), Write(delta_lambda_label))
        self.wait(2)

        # Add equation and explanation for epsilon
        epsilon_eq = MathTex(r"\varepsilon", r"=", r"\frac{\Delta\lambda}{\lambda}")
        epsilon_eq.to_edge(RIGHT, buff=0.5)
        epsilon_eq.to_edge(DOWN, buff=1)

        # Create a label for "row shift fraction"
        row_shift_label = Text("row shift fraction", font_size=20)

        # Get the position of the epsilon symbol more precisely
        epsilon_center = epsilon_eq[0].get_center()

        # Position the label above and to the left of epsilon
        row_shift_label.move_to(epsilon_center + UP * 1.2 + LEFT * 1.0)

        # Create the arrow from the label to epsilon
        arrow = Arrow(
            start=row_shift_label.get_bottom() + DOWN * 0.1,
            end=epsilon_center + UP * 0.1,  # Slight offset to point to top of epsilon
            buff=0.1,
            color=WHITE
        )

        # Animate the equation and explanation
        self.play(Write(epsilon_eq), Create(arrow), Write(row_shift_label), run_time=2)
        
        # End the animation with a longer wait (4 seconds total)
        self.wait(7)
    
    def create_curved_streamlines(self, entire_array, num_flow_lines=15):
        """Creates curved streamlines that navigate around the pillar array"""
        streamlines = VGroup()
        
        # Get array bounds
        array_left = entire_array.get_left()[0] - 0.5
        array_right = entire_array.get_right()[0] + 0.5
        array_top = entire_array.get_top()[1] + 0.5
        array_bottom = entire_array.get_bottom()[1] - 0.5
        
        # Create starting points at the top
        for i in range(num_flow_lines):
            # Distribute evenly across the width of the array
            x_pos = array_left + (array_right - array_left) * i / (num_flow_lines - 1)
            start_point = [x_pos, array_top + 1, 0]
            
            # Create a series of points to define the curved path
            points = [start_point]
            
            # Number of control points to add for the curve
            num_control_points = 12
            
            for j in range(1, num_control_points - 1):
                # Calculate y position interpolating from top to bottom
                y_pos = array_top + 1 - (j * ((array_top + 1) - (array_bottom - 1)) / (num_control_points - 1))
                
                # For even rows, add a slight rightward bias to simulate fluid flow around pillars
                # For odd rows, add a slight leftward bias
                if j % 2 == 0:
                    x_offset = 0.15 * np.sin(j * PI / 4)
                else:
                    x_offset = -0.15 * np.sin(j * PI / 4)
                
                # Add some randomness to the path
                x_random = 0.05 * np.random.randn()
                
                # Calculate new x position with offset
                new_x = x_pos + x_offset + x_random
                
                # Add the point to the path
                points.append([new_x, y_pos, 0])
            
            # Add final point at the bottom
            points.append([x_pos, array_bottom - 1, 0])
            
            # Instead of creating multiple bezier segments, create a single curve
            # Create a simple smooth path through the points
            streamline = VMobject(color=TEAL, stroke_width=1.5, stroke_opacity=0.8)
            streamline.set_points_smoothly(points)
            
            # Store the start point explicitly for easier access
            streamline.flow_start = points[0]
            
            streamlines.add(streamline)
        
        return streamlines
    
    def create_particles_on_streamlines(self, streamlines):
        """Creates particles positioned along streamlines"""
        particles = VGroup()
        particle_streamline_pairs = []
        particle_colors = [RED, YELLOW, GREEN]
        particle_sizes = [0.08, 0.06, 0.04]
        
        for streamline in streamlines:
            # Determine how many particles to place on this streamline (1-3)
            num_particles = np.random.randint(1, 4)
            
            for _ in range(num_particles):
                color_idx = np.random.randint(0, len(particle_colors))
                size_idx = np.random.randint(0, len(particle_sizes))
                
                # Create the particle
                particle = Dot(
                    radius=particle_sizes[size_idx],
                    color=particle_colors[color_idx],
                )
                
                # Position it at the start of the streamline
                # Use the first point of the streamline
                if hasattr(streamline, 'flow_start'):
                    # Use the explicitly stored start point if available
                    particle.move_to(streamline.flow_start)
                else:
                    # Otherwise try to get the first point from the points array
                    if len(streamline.points) > 0:
                        particle.move_to(streamline.points[0])
                    else:
                        # Fallback to a safe position at the top of the stream
                        particle.move_to(streamline.get_top())
                
                # Add the particle to our collections
                particles.add(particle)
                particle_streamline_pairs.append((particle, streamline))
        
        return particle_streamline_pairs


# To run this animation:
# manim -pql dldflow.py DeterministicLateralDisplacement