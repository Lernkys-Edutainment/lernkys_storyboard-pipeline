from pathlib import Path

# ============================================================
# Project Directories
# ============================================================

PROJECT_ROOT = Path(__file__).parent

DATA_DIR = PROJECT_ROOT / "data"

SCRIPTS_DIR = DATA_DIR / "scripts"

APPROVED_STORYBOARDS_DIR = DATA_DIR / "approved_storyboards"

OUTPUT_DIR = PROJECT_ROOT / "output"

CHROMA_DB_DIR = PROJECT_ROOT / "chroma_db"

# ============================================================
# Chroma Configuration
# ============================================================

COLLECTION_NAME = "storyboard_examples"

TOP_K = 3

# ============================================================
# LLM Configuration
# ============================================================

MODEL_NAME = "gpt-5.5"

TEMPERATURE = 0.3

SUPPORTED_EXTENSIONS = [".docx"]


# ============================================================
# Storyboard Generation Configuration
#
# Update these values before generating a new batch
# of storyboards.
#
# DO NOT change the variable names.
# ============================================================

# ------------------------------------------------------------
# Talking Head Configuration
# ------------------------------------------------------------

# Percentage of storyboard beats that should include
# a presenter / talking head.

TALKING_HEAD_PERCENTAGE = 40

TALKING_HEAD_GUIDELINE = f"""
Approximately {TALKING_HEAD_PERCENTAGE}% of the storyboard beats
should contain a presenter or talking head.

The remaining storyboard beats should primarily use:

• Illustrations
• Educational diagrams
• Animations
• Infographics
• Visual explanations
• Motion graphics

Only use talking heads when they improve learning or
help explain difficult concepts.
"""


# ------------------------------------------------------------
# Animation Complexity
# ------------------------------------------------------------

# Allowed Values:
#
# Low
# Medium
# High

ANIMATION_COMPLEXITY = "Low"

ANIMATION_COMPLEXITY_GUIDELINES = {

    "Low": """
Use mostly static visuals.

Guidelines:
• Minimal animation
• Simple transitions
• Static illustrations
• Limited camera movement
• Basic zoom and pan only
""",

    "Medium": """
Use moderately animated educational visuals.

Guidelines:
• Animated diagrams
• Moderate character movement
• Smooth transitions
• Camera zoom and pan where useful
• Balanced use of animation
• Educational motion graphics
""",

    "High": """
Use highly dynamic visuals.

Guidelines:
• Rich character animation
• Dynamic camera movement
• Multiple animated elements
• Complex scene transitions
• Highly engaging educational visuals
• Advanced motion graphics
"""
}


# ============================================================
# Batch Creative Brief
#
# Update these values for every new client or batch.
#
# Do NOT change the dictionary keys.
# ============================================================

CREATIVE_BRIEF = {

    # --------------------------------------------------------
    # Previous Context
    # --------------------------------------------------------

    "previous_context": """
This is  a teachers training module. They have already completed previous modules so dont repeat the same concepts. 
""",

    # --------------------------------------------------------
    # Storyboard Requirements
    # --------------------------------------------------------

    "storyboard_requirements": """
Generate engaging educational storyboards.

Requirements:

• Maintain visual consistency across all storyboard beats.

• Use clean educational illustrations.

• Highlight important concepts using OST.

• Synchronize visuals with narration.

• Avoid unnecessary decorative elements.

• Use arrows, labels and diagrams wherever appropriate.

• Every storyboard beat should have a clear educational purpose.

• Maintain continuity with previous storyboard scenes.

• Use smooth transitions between beats.

• Never generate visuals that contradict the narration.
""",

    # --------------------------------------------------------
    # Target Audience
    # --------------------------------------------------------

    "target_audience": "Teachers",

    # --------------------------------------------------------
    # Visual Style
    # --------------------------------------------------------

    "visual_style": "Modern 2D Educational Animation for adults"
}