import turtle
import random
import time

# Screen setup
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Happy New Year!")
screen.setup(width=800, height=600)

# Fireworks colors
colors = ["red", "blue", "green", "yellow", "purple", "orange", "pink", "white"]

# Function to draw a circle-like explosion
def draw_firework(x, y, color):
    firework = turtle.Turtle()
    firework.speed(0)
    firework.hideturtle()
    firework.penup()
    firework.goto(x, y)
    firework.pendown()
    firework.color(color)
    for _ in range(36):  # Draw multiple lines to simulate a firework
        firework.forward(100)
        firework.backward(100)
        firework.right(10)

# Function to create fireworks randomly
def create_fireworks():
    for _ in range(10):  # Number of fireworks
        x = random.randint(-300, 300)  # Random X position
        y = random.randint(-200, 200)  # Random Y position
        color = random.choice(colors)
        draw_firework(x, y, color)
        time.sleep(0.5)  # Pause between fireworks

# Display New Year Wishes
def new_year_wishes():
    writer = turtle.Turtle()
    writer.hideturtle()
    writer.color("gold")
    writer.penup()
    writer.goto(0, 0)
    writer.write("Happy New Year!", align="center", font=("Courier", 36, "bold"))
    time.sleep(3)

# Main execution
if __name__ == "__main__":
    create_fireworks()
    new_year_wishes()
    screen.mainloop()