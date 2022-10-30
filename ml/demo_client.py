import argparse

import requests

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                        prog = 'demo_client.py',
                        description = 'Simple utility for sending requests to the Posts\' sentiment analyser')
    parser.add_argument(
        '-t', 
        '--text', 
        dest='text', 
        type=str, 
        help="custom text to classify",
        default="What a crowd 🔥🔥🔥 Thank you Buenos Aires and everyone watching in cinemas around the world. More screenings on Saturday"
        )
    parser.add_argument(
        '--host', 
        dest='host', 
        type=str, 
        help="custom host",
        default="127.0.0.1"
        )
    parser.add_argument(
        '-p', 
        '--port', 
        dest='port', 
        type=str, 
        help="custom port",
        default="8080"
        )
    args = parser.parse_args()

    response = requests.post(
        f"http://{args.host}:{args.port}/classify",
        data={"text": args.text}
    )
    
    response_json = response.json()
    top_label = response_json[0][0]
    top_score = response_json[0][1]
    
    print(f"Input text: {args.text}")
    print(f"Code: {response.status_code}")
    print(f"Scores: {response_json}")
    print(f"Result: {top_label} ({top_score})")