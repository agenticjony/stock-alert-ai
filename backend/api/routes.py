import json
from fastapi import APIRouter
from screeners.engine import calculate_master_score
from services.ai_service import client

router = APIRouter()

@router.get("/scan/{symbol}")
def scan_stock(symbol: str):
    return calculate_master_score(symbol)

@router.get("/search")
def natural_language_search(q: str):
    # 1. Run our base screening system over the test universe
    test_basket = ["SOFI", "PLTR", "AMD", "NVDA", "CELH", "ELF", "IOT"]
    passed_candidates = []
    
    for ticker in test_basket:
        score_card = calculate_master_score(ticker)
        if score_card.get("status") == "PASSED ALL SCREENER FILTERS":
            passed_candidates.append(score_card)
            
    if not passed_candidates:
        return {"user_query": q, "results_count": 0, "matches": []}

    # 2. Minimize structural footprint safely using .get() fallbacks
    minimized_data = [
        {
            "ticker": c.get("ticker"),
            "score": c.get("ai_growth_score"),
            "signal": c.get("signal"),
            # Safe checks: reads 'reasons_summary', then falls back to 'strengths', or an empty list
            "strengths": c.get("reasons_summary") or c.get("strengths") or [],
            "metrics": c.get("fundamental_metrics")
        }
        for c in passed_candidates
    ]

    prompt = f"""
    The user is searching for: "{q}"
    
    Here are the filtered stocks that passed our core fundamental/technical screening system:
    {json.dumps(minimized_data, indent=2)}
    
    Filter, filter-out, or re-order this list to best match the user's intent. 
    Return a valid JSON array containing only the tickers that match. If none match the context well, return an empty array [].
    Do not wrap the output in markdown formatting code blocks (no ```json). Output raw text only.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a database router that returns clean JSON arrays of stock tickers."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        
        matching_tickers = json.loads(response.choices[0].message.content.strip())
        final_matches = [c for c in passed_candidates if c.get("ticker") in matching_tickers]
        
        return {
            "user_query": q,
            "results_count": len(final_matches),
            "matches": final_matches
        }
        
    except Exception as e:
        return {
            "user_query": q,
            "error": f"AI ranking fallback active: {str(e)}",
            "results_count": len(passed_candidates),
            "matches": passed_candidates
        }

        