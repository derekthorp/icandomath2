from manim import *
import numpy as np

class FlowLanesSimulation(Scene):
    def construct(self):
        # Configuration
        num_columns = 4
        num_rows = 3
        pillar_radius = 0.525  # Increased by 1.75x from original 0.3
        pillar_color = BLUE
        pillar_spacing_x = 5.0 * pillar_radius  # Further increased spacing between pillars
        pillar_spacing_y = 5.0 * pillar_radius  # Further increased spacing between rows
        
        # Calculate total width of the pillar array to center it
        total_width = (num_columns - 1) * pillar_spacing_x
        start_x = -total_width / 2
        
        # Calculate total height to position the array
        total_height = (num_rows - 1) * pillar_spacing_y
        start_y = total_height / 2
        
        # Create a group to hold all pillar rows
        all_pillar_rows = []
        
        # Create the pillar array with row shifts
        for row in range(num_rows):
            # Create a row group
            pillar_row = VGroup()
            
            # Calculate row offset - each row is shifted by lambda/4 compared to the previous row
            row_offset = row * (pillar_spacing_x / 4)
            
            # Calculate y position for this row
            row_y = start_y - (row * pillar_spacing_y)
            
            # Create pillars for this row
            for col in range(num_columns):
                x_pos = start_x + col * pillar_spacing_x + row_offset
                pillar = Circle(radius=pillar_radius, color=pillar_color, fill_opacity=0.8)
                pillar.move_to([x_pos, row_y, 0])
                pillar_row.add(pillar)
            
            # Add this row to our collection
            all_pillar_rows.append(pillar_row)
            
            # Add animation to reveal the row
            self.play(Create(pillar_row), run_time=0.7)
        
        self.wait(1)
        
        # Create a group containing all rows for easier reference
        entire_array = VGroup()
        for row in all_pillar_rows:
            entire_array.add(row)
        
        # Define the flow lanes with different colors (matching the screenshot)
        flow_lane_colors = [PINK, YELLOW]  # Reduced to two colors as per screenshot
        flow_lane_names = ["L1", "L2"]
        flow_lanes = VGroup()
        
        # Create the flow lanes with appropriate shifts
        array_top = entire_array.get_top()[1] + 0.5
        array_bottom = entire_array.get_bottom()[1] - 0.5
        
        # Track the paths of particles through the array for each lane
        lane_paths = []
        
        # Get first row pillars to place lanes between them
        first_row_pillars = all_pillar_rows[0]
        
        # MODIFIED: Both lanes start between the middle two pillars, but Lane 1 slightly to the left
        second_pillar_center = first_row_pillars[1].get_center()
        third_pillar_center = first_row_pillars[2].get_center()
        middle_x_start = (second_pillar_center[0] + third_pillar_center[0]) / 2
        
        # Lane 1 starts further to the left of the midpoint (doubled offset)
        lane1_x_start = middle_x_start - 0.4
        
        # Lane 1 (pink) - now starts slightly left of middle, shows zigzag behavior
        lane1_points = []
        # Starting point at the top
        lane1_points.append([lane1_x_start, array_top, 0])
        
        # For each row, calculate the position
        for row in range(num_rows + 1):
            if row < num_rows:
                # Get pillars in this row
                row_pillars = all_pillar_rows[row]
                y_pos = row_pillars[0].get_center()[1]
                
                if row == 0:
                    # For first row, use the slightly offset starting position
                    lane1_points.append([lane1_x_start, y_pos, 0])
                elif row == 1:
                    # For second row, position to hit the SECOND pillar (zigzag behavior)
                    # Position directly on the second pillar's center in the second row (the one circled in red)
                    second_pillar_pos = row_pillars[1].get_center()
                    lane1_points.append([second_pillar_pos[0], y_pos, 0])
                else:
                    # For third row, continue the zigzag pattern by positioning between pillars again
                    # Position between first and second pillar in the third row
                    first_pillar = row_pillars[0].get_center()
                    second_pillar = row_pillars[1].get_center()
                    x_pos = (first_pillar[0] + second_pillar[0]) / 2
                    lane1_points.append([x_pos, y_pos, 0])
            else:
                # Add a point at the bottom, continuing the same trajectory
                last_x = lane1_points[-1][0]
                second_last_x = lane1_points[-2][0]
                x_diff = last_x - second_last_x
                x_pos = last_x + x_diff  # Continue the same direction
                lane1_points.append([x_pos, array_bottom, 0])
        
        # Create the lane path
        lane1 = VMobject(color=flow_lane_colors[0], stroke_width=3)
        lane1.set_points_smoothly(lane1_points)
        flow_lanes.add(lane1)
        lane_paths.append(lane1_points)
        
        # Lane 2 (yellow) - still flows between second and third pillar, shows bounce behavior
        lane2_points = []
        # Starting point at the top, between second and third pillar (same as before)
        lane2_points.append([middle_x_start, array_top, 0])
        
        for row in range(num_rows + 1):
            if row < num_rows:
                row_pillars = all_pillar_rows[row]
                y_pos = row_pillars[0].get_center()[1]
                
                if row == 0:
                    # For first row, use the starting position
                    lane2_points.append([middle_x_start, y_pos, 0])
                else:
                    # For subsequent rows, position between second and third pillar (bounce behavior)
                    # This ensures lane 2 avoids hitting pillars
                    if row_pillars.length_over_dim(0) >= 3:  # Make sure we have enough pillars
                        second_pillar = row_pillars[1].get_center()
                        third_pillar = row_pillars[2].get_center()
                        x_pos = (second_pillar[0] + third_pillar[0]) / 2
                        lane2_points.append([x_pos, y_pos, 0])
                    else:
                        # Fallback if row doesn't have enough pillars
                        x_pos = lane2_points[-1][0]
                        lane2_points.append([x_pos, y_pos, 0])
            else:
                # Add a point at the bottom, continuing the same path
                last_x = lane2_points[-1][0]
                second_last_x = lane2_points[-2][0]
                x_diff = last_x - second_last_x
                x_pos = last_x - x_diff
                lane2_points.append([x_pos, array_bottom, 0])
        
        lane2 = VMobject(color=flow_lane_colors[1], stroke_width=3)
        lane2.set_points_smoothly(lane2_points)
        flow_lanes.add(lane2)
        lane_paths.append(lane2_points)
        
        # Display all the flow lanes
        self.play(Create(flow_lanes), run_time=1.5)
        
        # Add labels for each lane
        lane_labels = VGroup()
        
        for i, (lane, name) in enumerate(zip(flow_lanes, flow_lane_names)):
            # Position the label at the top of each lane
            label = Text(name, font_size=18, color=flow_lane_colors[i])
            label.next_to(lane.points[0], UP, buff=0.2)
            lane_labels.add(label)
        
        self.play(FadeIn(lane_labels))
        self.wait(1)
        
        # Create particles to animate along the lanes
        particles = VGroup()
        particle_lane_pairs = []
        
        for i, path_points in enumerate(lane_paths):
            # Create a particle for this lane
            particle = Dot(
                radius=0.08,
                color=flow_lane_colors[i],
                fill_opacity=1.0
            )
            
            # Position it at the start of the lane
            particle.move_to(path_points[0])
            particles.add(particle)
            
            # Create a mobject to animate along
            path = VMobject()
            path.set_points_smoothly(path_points)
            
            particle_lane_pairs.append((particle, path))
        
        # Add the particles to the scene
        self.play(FadeIn(particles))
        
        # Animate the particles along the lanes
        particle_animations = []
        
        for particle, path in particle_lane_pairs:
            animation = MoveAlongPath(particle, path, run_time=4)
            particle_animations.append(animation)
        
        # Play all particle animations simultaneously
        self.play(*particle_animations)
        
        # Add a label explaining the flow lanes behavior
        explanation = Text("Particles follow different flow paths", font_size=24)
        explanation.to_edge(DOWN, buff = 2.5)
        explanation.to_edge(LEFT, buff = .3)
        
        self.play(FadeIn(explanation))
        
        # Add lane numbers at the bottom of each lane
        bottom_labels = VGroup()
        
        for i, lane in enumerate(flow_lanes):
            # Get the position at the bottom of the lane
            bottom_pos = lane.points[-1]
            label = Text(f"{i+1}", font_size=18, color=flow_lane_colors[i])
            label.next_to(bottom_pos, DOWN, buff=0.2)
            bottom_labels.add(label)
        
        self.play(FadeIn(bottom_labels))
        
        # Create a legend to show lane behaviors
        legend_title = Text("Flow Lanes", font_size=20)
        legend_title.to_corner(UR, buff=0.75)
        
        legend_items = VGroup()
        legend_descriptions = [
            "Lane 1: Zigzag",
            "Lane 2: Bounce"
        ]
        
        for i, desc in enumerate(legend_descriptions):
            color_dot = Dot(radius=0.1, color=flow_lane_colors[i])
            text = Text(desc, font_size=14)
            text.next_to(color_dot, RIGHT, buff=0.2)
            item = VGroup(color_dot, text)
            legend_items.add(item)
        
        legend_items.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        legend_items.next_to(legend_title, DOWN, aligned_edge=LEFT, buff=0.2)
        
        legend = VGroup(legend_title, legend_items)
        self.play(FadeIn(legend))
        
        self.wait(2)
        
        # Final animation - let's show a second set of particles
        new_particles = VGroup()
        
        for i, path_points in enumerate(lane_paths):
            particle = Dot(
                radius=0.08,
                color=flow_lane_colors[i],
                fill_opacity=1.0
            )
            particle.move_to(path_points[0])
            new_particles.add(particle)
        
        self.play(FadeIn(new_particles))
        
        # Animate the new particles along the lanes
        new_animations = []
        
        for i, (particle, path) in enumerate(zip(new_particles, [p[1] for p in particle_lane_pairs])):
            animation = MoveAlongPath(particle, path, run_time=4)
            new_animations.append(animation)
        
        self.play(*new_animations)
        
        self.wait(1)
        
        # NEW ADDITION: Add a larger green particle that moves directly downward until hitting pillar
        # Calculate the position between the lanes at the top
        green_particle_x = (lane1_points[0][0] + lane2_points[0][0]) / 2
        green_particle_y = array_top  # Start at the top like other particles
        
        # Size it to overlap both lanes but still fit between the pillars
        green_particle_radius = 0.25  # Larger than regular particles but smaller than pillar gap
        
        # Create the green particle
        green_particle = Circle(
            radius=green_particle_radius,
            color=GREEN,
            fill_opacity=0.8,
            fill_color=GREEN_A
        )
        green_particle.move_to([green_particle_x, green_particle_y, 0])
        
        # Add the green particle to the scene
        self.play(FadeIn(green_particle))
        self.wait(5)
        
        # Create a path for the green particle that moves straight down until it hits the pillar
        green_path_points = []
        green_path_points.append([green_particle_x, green_particle_y, 0])  # Start at top
        
        # Get the target pillar in the second row
        target_pillar = all_pillar_rows[1][1]  # Second pillar in second row
        target_pillar_center = target_pillar.get_center()
        
        # Move straight down to the y-coordinate of the second row pillar
        # This ensures the particle moves directly downward in y-direction
        green_path_points.append([green_particle_x, target_pillar_center[1], 0])
        
        # Find where Lane 2 is at after the second row
        lane2_second_row_index = -1
        for i, point in enumerate(lane2_points):
            if abs(point[1] - target_pillar_center[1]) < 0.1:  # Close to pillar's y-coordinate
                lane2_second_row_index = i
                break
        
        # Add all Lane 2 points from after the second row
        for i in range(lane2_second_row_index + 1, len(lane2_points)):
            green_path_points.append(lane2_points[i])
        
        # Create the path
        green_path = VMobject()
        green_path.set_points_smoothly(green_path_points)
        
        # Animate the green particle along its path
        green_animation = MoveAlongPath(green_particle, green_path, run_time=3)
        self.play(green_animation)
        
        # Wait a moment to show the final positions
        self.wait(1)
        
        # Create dots at the end of each flow lane to match the screenshot
        end_dots = VGroup()
        for i, lane in enumerate(flow_lanes):
            # Get the end position of the lane
            end_pos = lane.points[-1]
            dot = Dot(
                point=end_pos,
                radius=0.1,
                color=flow_lane_colors[i],
                fill_opacity=1.0
            )
            end_dots.add(dot)
        
        # Add a green end dot for the green particle
        green_end_dot = Dot(
            point=green_path_points[-1],
            radius=0.1,
            color=GREEN,
            fill_opacity=1.0
        )
        end_dots.add(green_end_dot)
        
        self.play(FadeIn(end_dots))
        self.wait(1)
        
        # Fade out particles (including green particle) but keep the green particle visible
        self.play(
            FadeOut(new_particles),
            FadeOut(particles),
            FadeOut(explanation),
            FadeOut(legend),
            FadeOut(lane_labels),
            FadeOut(bottom_labels)
        )
        
        # Final view of just the device with flow paths and particles
        self.wait(2)


# To run this animation:
# manim -pql flowlanes.py FlowLanesSimulation
