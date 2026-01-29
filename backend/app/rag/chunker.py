def build_search_text(course, event, segment):
    return f"""
    Scenario: {event.get('scenario_title')}
    Description: {event.get('description')}
    Role: {event.get('context', {}).get('role')}
    Customer says: {segment.get('customer_utterance') or segment.get('employee_utterance')}
    Expected response: {segment.get('expected_response')}
    Emotion: {segment.get('customer_emotion') or segment.get('employee_emotion')}
    Tone: {segment.get('ideal_tone')}
    Objectives: {', '.join(event.get('objective', []))}
    """.strip()

def build_rag_chunks(raw_json):
    chunks = []

    for event in raw_json["events"]:
        for segment in event["segments"]:
            chunk = {
                "chunk_id": f"{raw_json['course_id']}_{event['event_id']}_segment_{segment['segment_id']}",
                "course_id": raw_json["course_id"],
                "event_id": event["event_id"],
                "scenario_title": event["scenario_title"],
                "segment_id": segment["segment_id"],
                "customer_utterance": segment.get("customer_utterance") or segment.get("employee_utterance"),
                "expected_response": segment["expected_response"],
                "emotion": segment.get("customer_emotion") or segment.get("employee_emotion"),
                "ideal_tone": segment.get("ideal_tone"),
                "objectives": event.get("objective", []),
                "search_text": build_search_text(raw_json, event, segment)
            }
            chunks.append(chunk)

    return chunks 