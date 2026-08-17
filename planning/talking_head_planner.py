import config


def create_talking_head_plan(beats: dict) -> dict:
    """
    Deterministically creates a visual plan assigning "Talking Head" or "Other"
    to each beat based on TALKING_HEAD_PERCENTAGE.

    Args:
        beats: Dictionary containing a "beats" key with a list of beat objects.

    Returns:
        A dictionary mapping beat IDs (and formatted keys) to visual types.
    """
    if isinstance(beats, dict) and "beats" in beats:
        beats_list = beats["beats"]
    else:
        beats_list = beats

    total_beats = len(beats_list)
    if total_beats == 0:
        return {}

    # Calculate target number of talking head beats
    num_talking_heads = round((config.TALKING_HEAD_PERCENTAGE / 100.0) * total_beats)
    num_talking_heads = max(0, min(total_beats, num_talking_heads))

    chosen_indices = set()
    if num_talking_heads > 0:
        # Centered Bresenham-like spacing to distribute K items in N slots
        spacing = total_beats / num_talking_heads
        offset = (spacing - 1) / 2.0
        for i in range(num_talking_heads):
            idx = int(round(i * spacing + offset))
            idx = max(0, min(total_beats - 1, idx))
            chosen_indices.add(idx)

    plan = {}
    for idx, beat in enumerate(beats_list):
        beat_id = beat.get("beat_id")
        visual_type = "Talking Head" if idx in chosen_indices else "Other"
        
        # Store using string representation of beat_id
        plan[str(beat_id)] = visual_type
        
        # Also store using "beat_00X" format if beat_id can be cast to int
        try:
            num = int(beat_id)
            plan[f"beat_{num:03d}"] = visual_type
        except (ValueError, TypeError):
            pass

    return plan
