from model_utils import Choices

EXERCISE_TYPE_CHOICES = Choices(
    ('S', 'Soccer'),
    ('W', 'Weightlifting'),
    ('C', 'Conditioning'),
    ('P', 'Plyometrics')
)

SOCCER_DRILL_TYPE_CHOICES = Choices(
    ('D', 'Dribbling'),
    ('S', 'Shooting'),
    ('C', 'Crossing'),
    ('P', 'Passing'),
    ('F', 'First Touch'),
    ('J', 'Juggling'),
    ('T', 'Tight Space')
)

WEIGHTLIFTING_TYPE_CHOICES = Choices(
    ('B', 'Bodyweight Training Session'),
    ('L', 'Legs'),
    ('P', 'Push'),
    ('U', 'Pull'),
    ('A', 'Accessory'),
    ('F', 'Full Body Workout')
)

CONDITIONING_TYPE_CHOICES = Choices(
    ('S', 'Short Distance'),
    ('M', 'Mid Distance'),
    ('L', 'Long Distance')
)

PLYOMETRIC_TYPE_CHOICES = Choices(
    ('A', 'Agility'),
    ('E', 'Explosiveness'),
    ('J', 'Jumping')
)

# WEEKDAY_CHOICES = Choices(
#     (0, 'Monday'),
#     (1, 'Tuesday'),
#     (2, 'Wednesday'),
#     (3, 'Thursday'),
#     (4, 'Friday'),
#     (5, 'Saturday'),
#     (6, 'Sunday')
# )

COLORS_CHOICES = Choices(
    ('R', 'Red'),
    ('W', 'White'),
    ('G', 'Gray'),
    ('B', 'Black')
)

ALL_EXERCISES_CHOICES = SOCCER_DRILL_TYPE_CHOICES + WEIGHTLIFTING_TYPE_CHOICES + CONDITIONING_TYPE_CHOICES + PLYOMETRIC_TYPE_CHOICES
