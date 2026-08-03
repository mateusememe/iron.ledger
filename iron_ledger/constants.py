BASE_URL = "https://api.hevyapp.com"

class Endpoints:
    ROUTINES = "/v1/routines"
    ROUTINE_FOLDERS = "/v1/routine_folders"
    EXERCISE_TEMPLATES = "/v1/exercise_templates"

class RateLimits:
    MAX_RETRIES = 5
    BASE_DELAY = 1.0
