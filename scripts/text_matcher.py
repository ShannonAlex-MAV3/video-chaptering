from difflib import SequenceMatcher
from typing import List, Dict, Any

def similar(a: str, b: str) -> float:
    """Calculate similarity ratio between two strings."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def clean_text(text: str) -> str:
    """Clean text by removing extra whitespace and converting to lowercase."""
    return ' '.join(text.lower().split())

def find_segment_indices(chapter_content: str, segments: List[Dict[str, Any]]) -> tuple:
    """
    Find the start and end segment indices for a chapter by comparing content similarity.
    Returns tuple of (start_index, end_index).
    """
    chapter_content = clean_text(chapter_content)
    best_start_idx = None
    best_end_idx = None
    best_start_score = 0.3  # Minimum similarity threshold
    
    # Find start index
    for i, segment in enumerate(segments):
        segment_text = clean_text(segment['text'])
        similarity = similar(chapter_content[:len(segment_text)], segment_text)
        
        if similarity > best_start_score:
            best_start_score = similarity
            best_start_idx = i
    
    if best_start_idx is None:
        return None, None
    
    # Find end index by accumulating text
    accumulated_text = ""
    for i in range(best_start_idx, len(segments)):
        accumulated_text += " " + clean_text(segments[i]['text'])
        if clean_text(chapter_content) in clean_text(accumulated_text):
            best_end_idx = i
            break
    
    return best_start_idx, best_end_idx

def align_chapters_with_whisper(gemma_chapters: List[Dict[str, Any]], 
                              whisper_segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Align Gemma 2 chapters with Whisper segments to get timestamps for each chapter.
    
    Args:
        gemma_chapters: List of chapters from Gemma 2 with chapterNumber, title, and content
        whisper_segments: List of Whisper segments with start, end, and text
    
    Returns:
        List of chapters with start and end timestamps
    """
    aligned_chapters = []
    current_segment_idx = 0
    
    for chapter in gemma_chapters:
        chapter_content = chapter["content"]
        
        # Find matching segments for this chapter
        start_idx, end_idx = find_segment_indices(
            chapter_content, 
            whisper_segments[current_segment_idx:]
        )
        
        if start_idx is not None and end_idx is not None:
            # Adjust indices based on current_segment_idx
            start_idx += current_segment_idx
            end_idx += current_segment_idx
            
            # Get timestamps
            start_time = whisper_segments[start_idx]["start"]
            end_time = whisper_segments[end_idx]["end"]
            
            # Update current_segment_idx for next iteration
            current_segment_idx = end_idx + 1
            
            # Create aligned chapter
            aligned_chapter = {
                "chapterNumber": chapter["chapterNumber"],
                "title": chapter["title"],
                "content": chapter_content,
                "start": start_time,
                "end": end_time,
                "segments": list(range(start_idx, end_idx + 1))  # Store segment indices for reference
            }
        else:
            # If no matching segments found, include chapter without timestamps
            aligned_chapter = {
                "chapterNumber": chapter["chapterNumber"],
                "title": chapter["title"],
                "content": chapter_content,
                "start": None,
                "end": None,
                "segments": []
            }
            
        aligned_chapters.append(aligned_chapter)
    
    return aligned_chapters

# Example usage:
if __name__ == "__main__":
    # Sample test with small data
    test_chapters = [
        {
            "chapterNumber": 1,
            "title": "What is Amazon Time Stream?",
            "content": "So now let's talk about Amazon time stream and the name indicates that it's actually a time series database So it's fully managed. It's fast. It's scalable and it's serverless So what is the time series? Well, it's a bunch of points that have a time included in them So for example here's a graph by year. So this is a time series now with time screen You can automatically adjust the database up and down to a scale capacity and you can store and analyze Trillions of events per day. The idea is that if you have a time series database It's going to be much faster and much cheaper than using relational databases for time series data Hence the specificity of having a time series database.",
            "startTime": "00:00"
        },
        {
            "chapterNumber": 2,
            "title": "Time Series Database Benefits",
            "content": "You can do schedule queries You can have records with multiple measures and there is full SQL compatibility The recent data it will be kept in memory and then the historical data is kept in a cost-automized storage tier As well as you have time series analytics function to help you analyze your data and find patterns in near real time This database just like every database on AWS supports encryption in transit and at rest So the use cases for time stream would be to have an IoT application Operational applications real-time analytics, but everything related to a time series database Now in terms of architecture time stream is here and it can receive data from AWS IoT so internet of things Can you see data streams through Lambda can receive data as well? Prometheus telegraph their integrations for that Can you see the streams as well through can you see data analytics for Apache flink can receive data into Amazon time stream and Amazon MSK as well through the same process and in terms of what can connect to time stream Well, we can build dashboards using Amazon quicksites We can do machine learning using Amazon SageMaker We can do graphana or because there is a standard JDBC connection into your database any application that is compatible with JDBC and SQL can leverage Amazon time stream So that's it. I think from the exam you just remember what time stream is at a high level But I want to give you a bit more details as well So that's it for this lecture.",
            "startTime": "04:31"
        }
    ]
    
    test_segments = [
        {
            "id": 0,
            "seek": 0,
            "start": 0.0,
            "end": 6.48,
            "text": " So now let's talk about Amazon time stream and the name indicates that it's actually a time series database",
            "tokens": [
                50364,
                407,
                586,
                718,
                311,
                751,
                466,
                6795,
                565,
                4309,
                293,
                264,
                1315,
                16203,
                300,
                309,
                311,
                767,
                257,
                565,
                2638,
                8149,
                50688
            ],
            "temperature": 0.0,
            "avg_logprob": -0.2155705349785941,
            "compression_ratio": 1.75,
            "no_speech_prob": 0.07008238881826401
        },
        {
            "id": 1,
            "seek": 0,
            "start": 6.48,
            "end": 9.72,
            "text": " So it's fully managed. It's fast. It's scalable and it's serverless",
            "tokens": [
                50688,
                407,
                309,
                311,
                4498,
                6453,
                13,
                467,
                311,
                2370,
                13,
                467,
                311,
                38481,
                293,
                309,
                311,
                7154,
                1832,
                50850
            ],
            "temperature": 0.0,
            "avg_logprob": -0.2155705349785941,
            "compression_ratio": 1.75,
            "no_speech_prob": 0.07008238881826401
        },
        {
            "id": 2,
            "seek": 0,
            "start": 9.96,
            "end": 15.96,
            "text": " So what is the time series? Well, it's a bunch of points that have a time included in them",
            "tokens": [
                50862,
                407,
                437,
                307,
                264,
                565,
                2638,
                30,
                1042,
                11,
                309,
                311,
                257,
                3840,
                295,
                2793,
                300,
                362,
                257,
                565,
                5556,
                294,
                552,
                51162
            ],
            "temperature": 0.0,
            "avg_logprob": -0.2155705349785941,
            "compression_ratio": 1.75,
            "no_speech_prob": 0.07008238881826401
        },
        {
            "id": 3,
            "seek": 0,
            "start": 15.96,
            "end": 21.080000000000002,
            "text": " So for example here's a graph by year. So this is a time series now with time screen",
            "tokens": [
                51162,
                407,
                337,
                1365,
                510,
                311,
                257,
                4295,
                538,
                1064,
                13,
                407,
                341,
                307,
                257,
                565,
                2638,
                586,
                365,
                565,
                2568,
                51418
            ],
            "temperature": 0.0,
            "avg_logprob": -0.2155705349785941,
            "compression_ratio": 1.75,
            "no_speech_prob": 0.07008238881826401
        },
        {
            "id": 4,
            "seek": 0,
            "start": 21.080000000000002,
            "end": 27.84,
            "text": " You can automatically adjust the database up and down to a scale capacity and you can store and analyze",
            "tokens": [
                51418,
                509,
                393,
                6772,
                4369,
                264,
                8149,
                493,
                293,
                760,
                281,
                257,
                4373,
                6042,
                293,
                291,
                393,
                3531,
                293,
                12477,
                51756
            ],
            "temperature": 0.0,
            "avg_logprob": -0.2155705349785941,
            "compression_ratio": 1.75,
            "no_speech_prob": 0.07008238881826401
        },
        {
            "id": 5,
            "seek": 2784,
            "start": 27.84,
            "end": 32.6,
            "text": " Trillions of events per day. The idea is that if you have a time series database",
            "tokens": [
                50364,
                1765,
                46279,
                295,
                3931,
                680,
                786,
                13,
                440,
                1558,
                307,
                300,
                498,
                291,
                362,
                257,
                565,
                2638,
                8149,
                50602
            ],
            "temperature": 0.0,
            "avg_logprob": -0.22083516214408128,
            "compression_ratio": 1.7300380228136882,
            "no_speech_prob": 0.0031571134459227324
        },
        {
            "id": 6,
            "seek": 2784,
            "start": 32.72,
            "end": 39.88,
            "text": " It's going to be much faster and much cheaper than using relational databases for time series data",
            "tokens": [
                50608,
                467,
                311,
                516,
                281,
                312,
                709,
                4663,
                293,
                709,
                12284,
                813,
                1228,
                38444,
                22380,
                337,
                565,
                2638,
                1412,
                50966
            ],
            "temperature": 0.0,
            "avg_logprob": -0.22083516214408128,
            "compression_ratio": 1.7300380228136882,
            "no_speech_prob": 0.0031571134459227324
        },
        {
            "id": 7,
            "seek": 2784,
            "start": 39.96,
            "end": 45.28,
            "text": " Hence the specificity of having a time series database. You can do schedule queries",
            "tokens": [
                50970,
                22229,
                264,
                2685,
                507,
                295,
                1419,
                257,
                565,
                2638,
                8149,
                13,
                509,
                393,
                360,
                7567,
                24109,
                51236
            ],
            "temperature": 0.0,
            "avg_logprob": -0.22083516214408128,
            "compression_ratio": 1.7300380228136882,
            "no_speech_prob": 0.0031571134459227324
        },
        {
            "id": 8,
            "seek": 2784,
            "start": 45.28,
            "end": 49.96,
            "text": " You can have records with multiple measures and there is full SQL compatibility",
            "tokens": [
                51236,
                509,
                393,
                362,
                7724,
                365,
                3866,
                8000,
                293,
                456,
                307,
                1577,
                19200,
                34237,
                51470
            ],
            "temperature": 0.0,
            "avg_logprob": -0.22083516214408128,
            "compression_ratio": 1.7300380228136882,
            "no_speech_prob": 0.0031571134459227324
        },
        {
            "id": 9,
            "seek": 2784,
            "start": 50.56,
            "end": 57.480000000000004,
            "text": " The recent data it will be kept in memory and then the historical data is kept in a cost-automized storage tier",
            "tokens": [
                51500,
                440,
                5162,
                1412,
                309,
                486,
                312,
                4305,
                294,
                4675,
                293,
                550,
                264,
                8584,
                1412,
                307,
                4305,
                294,
                257,
                2063,
                12,
                1375,
                298,
                1602,
                6725,
                12362,
                51846
            ],
            "temperature": 0.0,
            "avg_logprob": -0.22083516214408128,
            "compression_ratio": 1.7300380228136882,
            "no_speech_prob": 0.0031571134459227324
        },
        {
            "id": 10,
            "seek": 5748,
            "start": 57.959999999999994,
            "end": 65.24,
            "text": " As well as you have time series analytics function to help you analyze your data and find patterns in near real time",
            "tokens": [
                50388,
                1018,
                731,
                382,
                291,
                362,
                565,
                2638,
                15370,
                2445,
                281,
                854,
                291,
                12477,
                428,
                1412,
                293,
                915,
                8294,
                294,
                2651,
                957,
                565,
                50752
            ],
            "temperature": 0.0,
            "avg_logprob": -0.2561958362529804,
            "compression_ratio": 1.6849315068493151,
            "no_speech_prob": 0.0019627674482762814
        },
        {
            "id": 11,
            "seek": 5748,
            "start": 65.56,
            "end": 71.0,
            "text": " This database just like every database on AWS supports encryption in transit and at rest",
            "tokens": [
                50768,
                639,
                8149,
                445,
                411,
                633,
                8149,
                322,
                17650,
                9346,
                29575,
                294,
                17976,
                293,
                412,
                1472,
                51040
            ],
            "temperature": 0.0,
            "avg_logprob": -0.2561958362529804,
            "compression_ratio": 1.6849315068493151,
            "no_speech_prob": 0.0019627674482762814
        },
        {
            "id": 12,
            "seek": 5748,
            "start": 71.28,
            "end": 75.75999999999999,
            "text": " So the use cases for time stream would be to have an IoT application",
            "tokens": [
                51054,
                407,
                264,
                764,
                3331,
                337,
                565,
                4309,
                576,
                312,
                281,
                362,
                364,
                30112,
                3861,
                51278
            ],
            "temperature": 0.0,
            "avg_logprob": -0.2561958362529804,
            "compression_ratio": 1.6849315068493151,
            "no_speech_prob": 0.0019627674482762814
        },
        {
            "id": 13,
            "seek": 5748,
            "start": 76.36,
            "end": 81.52,
            "text": " Operational applications real-time analytics, but everything related to a time series database",
            "tokens": [
                51308,
                12480,
                1478,
                5821,
                957,
                12,
                3766,
                15370,
                11,
                457,
                1203,
                4077,
                281,
                257,
                565,
                2638,
                8149,
                51566
            ],
            "temperature": 0.0,
            "avg_logprob": -0.2561958362529804,
            "compression_ratio": 1.6849315068493151,
            "no_speech_prob": 0.0019627674482762814
        },
        {
            "id": 14,
            "seek": 8152,
            "start": 82.11999999999999,
            "end": 88.75999999999999,
            "text": " Now in terms of architecture time stream is here and it can receive data from AWS IoT so internet of things",
            "tokens": [
                50394,
                823,
                294,
                2115,
                295,
                9482,
                565,
                4309,
                307,
                510,
                293,
                309,
                393,
                4774,
                1412,
                490,
                17650,
                30112,
                370,
                4705,
                295,
                721,
                50726
            ],
            "temperature": 0.0,
            "avg_logprob": -0.3169558525085449,
            "compression_ratio": 1.9260869565217391,
            "no_speech_prob": 0.023287033662199974
        },
        {
            "id": 15,
            "seek": 8152,
            "start": 89.44,
            "end": 92.52,
            "text": " Can you see data streams through Lambda can receive data as well?",
            "tokens": [
                50760,
                1664,
                291,
                536,
                1412,
                15842,
                807,
                45691,
                393,
                4774,
                1412,
                382,
                731,
                30,
                50914
            ],
            "temperature": 0.0,
            "avg_logprob": -0.3169558525085449,
            "compression_ratio": 1.9260869565217391,
            "no_speech_prob": 0.023287033662199974
        },
        {
            "id": 16,
            "seek": 8152,
            "start": 92.92,
            "end": 95.47999999999999,
            "text": " Prometheus telegraph their integrations for that",
            "tokens": [
                50934,
                2114,
                649,
                42209,
                4304,
                34091,
                641,
                3572,
                763,
                337,
                300,
                51062
            ],
            "temperature": 0.0,
            "avg_logprob": -0.3169558525085449,
            "compression_ratio": 1.9260869565217391,
            "no_speech_prob": 0.023287033662199974
        },
        {
            "id": 17,
            "seek": 8152,
            "start": 96.0,
            "end": 103.19999999999999,
            "text": " Can you see the streams as well through can you see data analytics for Apache flink can receive data into Amazon time stream and",
            "tokens": [
                51088,
                1664,
                291,
                536,
                264,
                15842,
                382,
                731,
                807,
                393,
                291,
                536,
                1412,
                15370,
                337,
                46597,
                932,
                475,
                393,
                4774,
                1412,
                666,
                6795,
                565,
                4309,
                293,
                51448
            ],
            "temperature": 0.0,
            "avg_logprob": -0.3169558525085449,
            "compression_ratio": 1.9260869565217391,
            "no_speech_prob": 0.023287033662199974
        },
        {
            "id": 18,
            "seek": 8152,
            "start": 103.52,
            "end": 108.8,
            "text": " Amazon MSK as well through the same process and in terms of what can connect to time stream",
            "tokens": [
                51464,
                6795,
                7395,
                42,
                382,
                731,
                807,
                264,
                912,
                1399,
                293,
                294,
                2115,
                295,
                437,
                393,
                1745,
                281,
                565,
                4309,
                51728
            ],
            "temperature": 0.0,
            "avg_logprob": -0.3169558525085449,
            "compression_ratio": 1.9260869565217391,
            "no_speech_prob": 0.023287033662199974
        },
        {
            "id": 19,
            "seek": 10880,
            "start": 108.96,
            "end": 111.96,
            "text": " Well, we can build dashboards using Amazon quicksites",
            "tokens": [
                50372,
                1042,
                11,
                321,
                393,
                1322,
                8240,
                17228,
                1228,
                6795,
                1702,
                82,
                3324,
                50522
            ],
            "temperature": 0.0,
            "avg_logprob": -0.2439546738901446,
            "compression_ratio": 1.6822742474916388,
            "no_speech_prob": 0.002589443465694785
        },
        {
            "id": 20,
            "seek": 10880,
            "start": 112.12,
            "end": 114.75999999999999,
            "text": " We can do machine learning using Amazon SageMaker",
            "tokens": [
                50530,
                492,
                393,
                360,
                3479,
                2539,
                1228,
                6795,
                33812,
                44,
                4003,
                50662
            ],
            "temperature": 0.0,
            "avg_logprob": -0.2439546738901446,
            "compression_ratio": 1.6822742474916388,
            "no_speech_prob": 0.002589443465694785
        },
        {
            "id": 21,
            "seek": 10880,
            "start": 114.92,
            "end": 122.36,
            "text": " We can do graphana or because there is a standard JDBC connection into your database any application that is compatible with JDBC and",
            "tokens": [
                50670,
                492,
                393,
                360,
                4295,
                2095,
                420,
                570,
                456,
                307,
                257,
                3832,
                37082,
                7869,
                4984,
                666,
                428,
                8149,
                604,
                3861,
                300,
                307,
                18218,
                365,
                37082,
                7869,
                293,
                51042
            ],
            "temperature": 0.0,
            "avg_logprob": -0.2439546738901446,
            "compression_ratio": 1.6822742474916388,
            "no_speech_prob": 0.002589443465694785
        },
        {
            "id": 22,
            "seek": 10880,
            "start": 122.64,
            "end": 125.24,
            "text": " SQL can leverage Amazon time stream",
            "tokens": [
                51056,
                19200,
                393,
                13982,
                6795,
                565,
                4309,
                51186
            ],
            "temperature": 0.0,
            "avg_logprob": -0.2439546738901446,
            "compression_ratio": 1.6822742474916388,
            "no_speech_prob": 0.002589443465694785
        },
        {
            "id": 23,
            "seek": 10880,
            "start": 125.72,
            "end": 129.88,
            "text": " So that's it. I think from the exam you just remember what time stream is at a high level",
            "tokens": [
                51210,
                407,
                300,
                311,
                309,
                13,
                286,
                519,
                490,
                264,
                1139,
                291,
                445,
                1604,
                437,
                565,
                4309,
                307,
                412,
                257,
                1090,
                1496,
                51418
            ],
            "temperature": 0.0,
            "avg_logprob": -0.2439546738901446,
            "compression_ratio": 1.6822742474916388,
            "no_speech_prob": 0.002589443465694785
        },
        {
            "id": 24,
            "seek": 10880,
            "start": 129.88,
            "end": 131.96,
            "text": " But I want to give you a bit more details as well",
            "tokens": [
                51418,
                583,
                286,
                528,
                281,
                976,
                291,
                257,
                857,
                544,
                4365,
                382,
                731,
                51522
            ],
            "temperature": 0.0,
            "avg_logprob": -0.2439546738901446,
            "compression_ratio": 1.6822742474916388,
            "no_speech_prob": 0.002589443465694785
        },
        {
            "id": 25,
            "seek": 10880,
            "start": 132.35999999999999,
            "end": 136.6,
            "text": " So that's it for this lecture. I hope you liked it and I will see you in the next lecture",
            "tokens": [
                51542,
                407,
                300,
                311,
                309,
                337,
                341,
                7991,
                13,
                286,
                1454,
                291,
                4501,
                309,
                293,
                286,
                486,
                536,
                291,
                294,
                264,
                958,
                7991,
                51754
            ],
            "temperature": 0.0,
            "avg_logprob": -0.2439546738901446,
            "compression_ratio": 1.6822742474916388,
            "no_speech_prob": 0.002589443465694785
        }
    ]
    
    result = align_chapters_with_whisper(test_chapters, test_segments)
    print(result)