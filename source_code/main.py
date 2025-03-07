import pandas as pd
import os
import re
from number_parser import parse_number
from datefinder import find_dates
from dateutil import tz
import re
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

##################################################
####### Load and Preprocess Haunted Places #######
##################################################

# Define file paths (assuming relative paths)
data_dir = os.path.join("..", "data", "raw")  # Ensure saving in "raw"
processed_dir = os.path.join("..", "data", "processed")

# Ensure directories exist
os.makedirs(processed_dir, exist_ok=True)

# Define file paths
input_file = os.path.join(data_dir, "haunted_places.tsv")
output_file = os.path.join(processed_dir, "non_ai_analysis.tsv")

# Check if the file exists
if not os.path.exists(input_file):
    print(f"Error: File not found at {os.path.abspath(input_file)}")
    exit(1)

# Load TSV file
df = pd.read_csv(input_file, sep="\t")
print(f"Loaded dataset: {input_file}")

# Ensure 'description' column exists
if "description" not in df.columns:
    print("Error: 'description' column missing in the dataset.")
    exit(1)

##################################################
################ Feature Engineering #############
##################################################

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Define keywords for feature extraction
audio_keywords = [
    "noises", "whisper", "footsteps", "screaming", "crying", "voices", "heard", "voice",
    "scream", "yell", "cry", "speak", "sob", "moan", "groan", "whimper", "shout", "murmur",
    "chant", "howl", "echo", "banging", "knocking", "humming", "singing", "wailing",
    "clanking", "rustling", "whistling", "creaking", "breathing", "gasping", "thumping",
    "rattling", "pounding", "drumming", "chanting", "growling", "scraping", "whining",
    "disembodied voice", "unnatural sound", "strange noises"
]


visual_keywords = [
    "see", "shadow", "figure", "glowing", "orbs", "apparition", "ghostly", "spotted",
    "saw", "viewed", "observed", "watched", "noticed", "sighted", "witnessed", "perceived",
    "discerned", "detected", "glimpsed", "beheld", "ghastly", "specter", "entity", "outline",
    "phantom", "manifestation", "flickering", "translucent", "shape", "silhouette", "misty",
    "blurred figure", "ethereal form", "wisp", "floating shape", "vapor", "smoky figure",
    "pale apparition", "shimmering light", "distorted reflection", "unusual movement",
    "shadowy figure", "dark form", "figure in the corner", "disappearing entity", "bright flash"
]


witness_keywords = [
    "witness", "witnesses", "people saw", "group saw", "several reported", "locals say",
    "locals report", "many claim", "it is said", "some say", "people claim", "they saw",
    "someone saw", "eyewitness", "reports suggest", "many believe", "accounts describe",
    "locals recall", "multiple reports", "testimonies state", "neighbors witnessed",
    "townspeople say", "villagers recall", "historical accounts", "folklore mentions",
    "urban legend", "word of mouth", "locals whisper", "unverified reports", "rumors suggest"
]

apparition_categories = {
    "Ghost": [
        "ghost", "apparition", "haunt", "presence", "disembodied", "phantom", "wraith",
        "specter", "manifest", "spirit", "floating", "see-through", "ethereal", "vapor",
        "transparent", "echo", "shade", "misty", "cold spot", "unseen", "voice", "presence",
        "energy", "unrest", "unearthly", "roaming", "wandering", "lost soul", "residual",
        "intelligent haunt", "invisible", "unknown", "shadowy", "lurking", "dead", "flickering",
        "mysterious", "ectoplasm", "full body", "partial", "formless", "entity", "illusion",
        "glowing", "gossamer", "orb", "vague", "spectral", "translucent", "seeable", "sensed",
        "blurred"
    ],

    "Spirit": [
        "spirit", "ethereal", "supernatural", "float", "aura", "presence", "immortal", "guardian",
        "wandering", "energy", "soul", "afterlife", "beyond", "angelic", "residual", "intelligent",
        "astral", "light being", "seer", "wisdom", "mystic", "enlighten", "guide", "sacred",
        "vision", "deity", "divine", "spectral", "unbodied", "manifest", "roaming", "medium",
        "whisper", "holy", "vessel", "unseen", "mystical", "presence", "seer", "force", "beyond",
        "prophet", "shimmer", "guardian", "enlightened", "transcend", "immaterial", "phantasmal",
        "unworldly", "anima"
    ],

    "Demonic Entity": [
        "demon", "shadow", "poltergeist", "revenant", "ghoul", "undead", "hellhound", "evil",
        "malevolent", "hellfire", "infernal", "satanic", "cursed", "possess", "torment", "suffer",
        "fiend", "wicked", "darkness", "ominous", "fiery", "devilish", "bloodcurdling", "shadowy",
        "nightmare", "inferno", "supernatural", "abomination", "ghastly", "fearsome", "necromancer",
        "diabolic", "phantasmal", "accursed", "twisted", "devil", "summon", "despair", "harrowing",
        "demonic", "screech", "chaos", "curse", "devour", "stalker", "phantom", "vile", "forbidden",
        "undead", "banshee", "wraith"
    ],

    "Mythological Creature": [
        "banshee", "wraith", "shade", "cryptid", "doppelganger", "fairy", "pixie", "leprechaun",
        "elf", "sprite", "nymph", "sylph", "troll", "giant", "goblin", "mermaid", "sirena", "selkie",
        "kraken", "dragon", "griffin", "unicorn", "werewolf", "shapeshifter", "changeling", "centaur",
        "minotaur", "phoenix", "kelpie", "chimera", "gorgon", "medusa", "hydra", "yeti", "sasquatch",
        "bigfoot", "loch ness", "wendigo", "manticore", "djinn", "harpy", "cyclops", "golem", "satyr",
        "chupacabra", "kitsune", "gargoyle", "frost giant", "lycan", "yokai"
    ],

    "Celestial Being": [
        "angel", "djinn", "jinn", "seraph", "cherub", "archangel", "guardian", "heavenly", "divine",
        "holy", "halo", "miracle", "savior", "prophet", "messenger", "pure", "light bearer", "radiant",
        "wings", "celestial", "choir", "luminescent", "shining", "bright", "immortal", "resurrect",
        "sacred", "piety", "ethereal", "spiritual", "godlike", "divinity", "tranquil", "mystical",
        "otherworldly", "sanctified", "blessing", "peaceful", "guardian spirit", "mystical", "glowing",
        "shimmering", "spiritual realm", "high being", "watcher", "miraculous", "protective", "faith"
    ],

    "Extraterrestrial": [
        "ufo", "orb", "paranormal", "otherworldly", "alien", "abduction", "probe", "flying", "cosmic",
        "interdimensional", "unknown", "spaceship", "craft", "beacon", "signal", "nonhuman", "unearthly",
        "hybrid", "telepathic", "advanced", "mystic", "men in black", "glowing", "meteor", "starship",
        "lightspeed", "warp", "vortex", "unexplainable", "celestial", "distant", "light entity", "hover",
        "void", "exoplanet", "reptilian", "gray alien", "cosmos", "nebula", "galactic", "transcend",
        "humanoid", "dimension", "frequency", "signal", "hyperjump", "abnormal", "nonphysical"
    ],

    "Misty Figure": [
        "mist", "specter", "phantom", "fog", "haze", "cloudy", "ethereal", "shadowy", "floating", "ghostly",
        "blurry", "vague", "translucent", "vapor", "mysterious", "formless", "silhouette", "shimmer", "wisp",
        "veil", "sway", "drifting", "cloud", "enigma", "swirl", "airy", "fluid", "thin", "partial", "unfocused",
        "soft", "radiant", "dim", "indistinct", "faint", "wavering", "otherworldly", "haunting", "obscure",
        "twilight", "melting", "diffuse", "glowing", "shimmering", "veil", "glimpse", "recede", "nocturnal",
        "hidden", "looming"
    ]
}

# Define event type keywords with root words only
event_keywords = {
    "Violent Deaths": [
        "murder", "homicide", "kill", "manslaughter", "assassinate", "bloodshed",
        "butcher", "slaughter", "stab", "shoot", "gun", "strangle", "beat", "lynch",
        "execute", "massacre", "behead", "decapitate", "bludgeon", "choke", "slit",
        "knife", "bullet", "shotgun", "rifle", "assault", "torture", "brutality",
        "mutilate", "ambush", "hostage", "violent", "throat", "disfigure", "garrote",
        "hack", "pierce", "maim", "gore", "carnage", "assail", "shooter", "gory",
        "shank", "crush", "beatdown", "assassin", "exterminate", "bloodlust", "stomp"
    ],

    "Suicide & Tragic Deaths": [
        "suicide", "hang", "self-inflict", "overdose", "poison", "self-harm",
        "jump", "drown", "fall", "leap", "self-destruct", "self-slaughter",
        "self-kill", "gas", "suffocate", "asphyxiate", "cut", "wrist", "slash",
        "drain", "self-strangle", "firearm", "self-gun", "shoot", "self-terminate",
        "pesticide", "cyanide", "lethal", "sedative", "depress", "goodbye", "tragic",
        "despair", "horrific", "tragic fate", "hopeless", "end life", "perish",
        "leave world", "harm oneself", "deadly intent", "end suffering", "grief",
        "intoxicate", "narcotic", "drug abuse", "self-violence", "final act", "farewell"
    ],

    "Accidents & Natural Disasters": [
        "accident", "drown", "burn", "crash", "electrocute", "fall", "misadventure",
        "bury", "explode", "gas", "collapse", "fire", "wildfire", "earthquake", "flood",
        "tornado", "hurricane", "tsunami", "avalanche", "landslide", "sinkhole",
        "volcano", "erupt", "storm", "lightning", "blizzard", "frostbite", "heatstroke",
        "hailstorm", "mudslide", "cyclone", "typhoon", "meteor", "acid rain", "drought",
        "heatwave", "flash flood", "power outage", "building collapse", "bridge fall",
        "factory explosion", "mine collapse", "industrial accident", "oil spill",
        "chemical leak", "dam burst", "stampede", "suffocation", "debris fall"
    ],

    "Unsolved & Mysterious Events": [
        "disappear", "vanish", "missing", "trace", "mystery", "unknown",
        "lost", "no evidence", "never seen", "no body", "no remains",
        "unexplained", "unsolved", "gone", "secret", "forbidden", "hidden",
        "enigma", "riddle", "unanswered", "strange", "peculiar", "otherworldly",
        "anomaly", "inexplicable", "supernatural", "bizarre", "unsuspected",
        "elusive", "legend", "folklore", "urban legend", "conspiracy", "cover-up",
        "vanished without trace", "erased", "eradicated", "never found", "fugitive",
        "abduct", "stolen identity", "unknown history", "untold story", "top secret",
        "disoriented", "never returned", "isolated", "cipher", "archived", "hidden past"
    ],

    "Paranormal & Supernatural Deaths": [
        "curse", "sacrifice", "ritual", "occult", "witchcraft", "haunt",
        "paranormal", "exorcism", "possess", "shadow", "supernatural",
        "hex", "spell", "voodoo", "mystic", "eldritch", "incantation",
        "conjure", "ghostly", "phantom", "ethereal", "mystical", "summon",
        "spiritual", "dark force", "unholy", "haunting", "astral", "medium",
        "beyond", "undead", "necromancer", "ritualistic", "seance", "ouija",
        "coven", "forbidden knowledge", "eldritch horror", "dark entity",
        "witch hunt", "haunted ground", "restless soul", "specter", "ritual murder",
        "poltergeist", "demonic force", "haunted house", "whispering spirits"
    ],

    "Unnatural & Suspicious Deaths": [
        "corpse", "remains", "skeletal", "decomposed", "gruesome", "mutilate",
        "mystery illness", "unexplained", "fatality", "body found", "cadaver",
        "body parts", "bloodstain", "no explanation", "horrific scene",
        "autopsy", "body dismember", "crime scene", "blood spatter", "post-mortem",
        "unknown cause", "suspicious", "no suspects", "bruises", "forensic",
        "morgue", "unmarked grave", "decay", "rotting", "discarded remains",
        "mysterious end", "concealed", "unclaimed", "lifeless", "severed",
        "violent marks", "unregistered", "unknown figure", "cold case", "evidence missing",
        "foul play", "hidden corpse", "corpse relocation", "clandestine", "deep cuts"
    ],

    "Torture & Extreme Crimes": [
        "torture", "suffer", "agonizing", "brutal", "disembowel", "skinned",
        "sacrifice", "ritual pain", "slow death", "painful", "mutilation",
        "gut", "torment", "sadistic", "bleed", "force-fed", "peel", "rip",
        "flay", "stretch", "lash", "whip", "scald", "burnt alive", "acid",
        "force drown", "stab repeatedly", "limb removal", "suffocate",
        "starve", "maimed", "harsh suffering", "ripped apart", "chained",
        "nail", "injection", "immobilized", "disfigure", "twist", "crucify",
        "teeth pull", "branded", "deformed", "flogged", "beaten beyond recognition"
    ],

    "Execution & Historical Deaths": [
        "execution", "hanging", "public execution", "guillotine", "burned at stake",
        "witch trial", "historic penalty", "beheading", "firing squad", "drawn",
        "quartered", "choke rope", "death sentence", "public display", "historical torture",
        "hanging tree", "royal punishment", "shameful death", "mob justice", "gruesome end",
        "dead man walking", "dungeon death", "scaffold", "axeman", "death decree",
        "stoned", "crushed to death", "punishment for crime", "soldier's execution",
        "war tribunal", "sacrificial burning", "trial by fire", "poison cup",
        "gladiator death", "forced duel", "imperial justice", "decimation",
        "ritual suicide", "exile execution", "public flogging", "death chamber",
        "horrible fate", "official sentencing", "historical hanging", "bludgeoning"
    ]
}


time_keywords = {
    "Morning": [
        "morning", "sunrise", "dawn", "daybreak", "breakfast", "early", "first light",
        "cockcrow", "sunup", "morning dew", "before noon", "early hours", "early morning",
        "sunray", "sun peeking", "morning mist", "rooster crow", "misty dawn",
        "fresh air", "dew drop", "sun breaking", "day begins", "faint light",
        "early brightness", "misty glow", "morning glow", "chirping birds", "soft sun",
        "morning hush", "waking world", "beginning of day", "calm light", "breeze of dawn",
        "half-light", "rosy-fingered dawn", "new day", "golden sunrise", "brisk morning",
        "awakening", "stretch of day", "orange sky", "soft awakening", "yawning earth",
        "silent morning", "mild sun", "morning shadow", "early twinkle", "horizon glow",
        "first warmth", "morning haze", "glistening sunrise"
    ],

    "Afternoon": [
        "afternoon", "midday", "pm", "noon", "lunch", "brunch", "high noon", "early afternoon",
        "mid-afternoon", "1 PM", "2 PM", "3 PM", "4 PM", "siesta", "brightest sun",
        "lunch hour", "zenith", "hot sun", "midday glow", "afternoon light", "golden afternoon",
        "lazy afternoon", "midday heat", "shade-seeking", "warmest hour", "slow afternoon",
        "baking heat", "hottest time", "sluggish air", "post-lunch", "calm noon",
        "midday slumber", "post-brunch", "crisp shadows", "long afternoon", "golden rays",
        "quiet noon", "tranquil moment", "stretching light", "hazy afternoon", "blue sky",
        "slow-moving day", "peak brightness", "mid-sun", "deepest blue", "longest shadows",
        "midway through", "after-lunch haze", "peaceful hour", "breezy noon"
    ],

    "Evening": [
        "evening", "dusk", "twilight", "sunset", "golden hour", "dinner", "supper",
        "late evening", "after work", "early evening", "gloaming", "6 PM", "7 PM", "8 PM",
        "cool air", "orange sky", "purple haze", "evening breeze", "mild warmth",
        "transition hour", "low sun", "sinking sun", "shifting light", "soft twilight",
        "evening hush", "quiet hours", "blue dusk", "long shadows", "evening shadow",
        "mellow glow", "moon rising", "waning light", "chilly air", "evening glow",
        "softening sky", "vanishing sun", "dim sky", "evening hush", "tired sun",
        "evening lull", "crimson sky", "fading warmth", "early starlight",
        "darkening hour", "end of day", "peaceful dusk", "sunset glow", "cooling day",
        "deep shadows", "twinkling sky", "serene twilight"
    ],

    "Night": [
        "night", "midnight", "dark", "late night", "starlight", "moonlight", "sleep", "dream",
        "wee hours", "after midnight", "3 AM", "4 AM", "2 AM", "dead of night", "witching hour",
        "nightfall", "pre-dawn", "before sunrise", "deep dark", "silent world", "cold air",
        "moon glow", "night breeze", "nocturnal hush", "shimmering stars", "night chill",
        "haunting silence", "midnight hour", "owl hoot", "shadowed world", "midnight glow",
        "whispering dark", "velvet sky", "faint shadows", "dark hush", "deep black",
        "glowing moon", "hushed tones", "restful quiet", "ethereal night", "ghostly glow",
        "muffled echoes", "dark expanse", "distant howls", "deepest hours", "unseen shadows",
        "endless sky", "lunar glow", "twilight hush", "fading echoes", "midnight chill"
    ]
}



# Functions to extract features
def contains_keywords(text, keywords):
    """Returns True if any keyword appears in the text."""
    if pd.isna(text):
        return False
    return any(re.search(rf"\b{keyword}\b", text, re.IGNORECASE) for keyword in keywords)


def extract_witness_count(text):
    """Extracts witness count from text, detecting both digits and written numbers."""
    if pd.isna(text) or text.strip() == "":
        return 0

    # Extract numbers written as digits (e.g., "3", "20")
    digit_numbers = [int(num) for num in re.findall(r'\b\d+\b', text)]

    # Extract written numbers using parse_number
    try:
        word_number = parse_number(text)
        if word_number is not None:
            digit_numbers.append(int(word_number))
    except:
        pass  # Ensure robustness in case of parsing errors

    return max(digit_numbers) if digit_numbers else 0  # Return the highest number


def extract_apparition_type(text):
    """Identifies apparition type from description using categorized keywords."""
    if pd.isna(text):
        return "Unknown"

    text = text.lower()
    matched_categories = set()

    # Check for matches in each category
    for category, keywords in apparition_categories.items():
        if any(re.search(rf"\b{re.escape(keyword)}\b", text) for keyword in keywords):
            matched_categories.add(category)

    return ", ".join(matched_categories) if matched_categories else "Unknown"



def extract_event_type(text):
    """Extract event types from a given text by checking event keywords."""
    if pd.isna(text):
        return "Unknown"

    text = text.lower()
    matched_categories = set()

    for category, keywords in event_keywords.items():
        if any(re.search(rf"\b{keyword}\b", text) for keyword in keywords):
            matched_categories.add(category)

    return ", ".join(matched_categories) if matched_categories else "Unknown"


def extract_time_of_day(text):
    """Identifies if the sighting happened in morning, afternoon, evening, or night."""
    if pd.isna(text):
        return "Unknown"

    for time_period, keywords in time_keywords.items():
        if any(re.search(rf"\b{keyword}\b", text, re.IGNORECASE) for keyword in keywords):
            return time_period
    return "Unknown"

def extract_date(text):
    """Extracts the latest date from text using datefinder, ensuring consistent timezone handling."""
    if pd.isna(text):
        return None

    matches = list(find_dates(text))

    # Ensure all dates are naive (remove timezone info if present)
    processed_dates = []
    for date in matches:
        if date.tzinfo is not None:
            date = date.astimezone(tz.UTC).replace(tzinfo=None)  # Convert to UTC and make it naive
        processed_dates.append(date)

    return max(processed_dates).strftime("%Y-%m-%d") if processed_dates else None


##################################################
####### Apply Feature Engineering ################
##################################################

df["Audio_Evidence"] = df["description"].apply(lambda x: contains_keywords(x, audio_keywords))
df["Visual_Evidence"] = df["description"].apply(lambda x: contains_keywords(x, visual_keywords))
df["Witness_Count"] = df["description"].apply(extract_witness_count)
df["Apparition_Type"] = df["description"].apply(extract_apparition_type)
df["Event_Type"] = df["description"].apply(extract_event_type)
df["Time_of_Day"] = df["description"].apply(extract_time_of_day)
df["Haunted_Place_Date"] = df["description"].apply(extract_date)

##################################################
####### Save the Enriched Dataset ################
##################################################

df.to_csv(output_file, sep="\t", index=False)
print(f"Feature engineering completed! Enriched dataset saved at: {output_file}")
