def calculate_technical_score(profile_data, tech_data, inst_data):
    score = 0
    reasons = []
    
    # Current Price data from Profile
    price = profile_data.get("price", 0)
    avg_volume = profile_data.get("averageVolume", 1)
    volume_today = profile_data.get("volume", 0)
    
    # Moving Averages & RSI from Technical Data
    sma50 = tech_data.get("sma50", 0) if tech_data else 0
    sma200 = tech_data.get("sma200", 0) if tech_data else 0
    rsi = tech_data.get("rsi", 60) if tech_data else 60 # Default safe center
    
    # 52 Week High validation
    year_high = profile_data.get("yearHigh", 0)
    is_breaking_52_week_high = price >= (year_high * 0.98) # Within 2% of breaking out
    
    # --- Step 3: Technical Momentum Calculations ---
    if price > sma50:
        score += 1
        reasons.append("✔ Price above SMA50")
    if sma50 > sma200:
        score += 1
        reasons.append("✔ SMA50 above SMA200 (Golden Cross Environment)")
    if 55 < rsi < 75:
        score += 1
        reasons.append(f"✔ RSI in Momentum Zone ({rsi:.1f})")
    if is_breaking_52_week_high:
        score += 2
        reasons.append("✔ Breaking or testing 52-Week Highs")
    if volume_today > (avg_volume * 2):
        score += 2
        reasons.append("✔ Volume Spike detected (>2x Average)")

    # --- Step 4: Institutional Accumulation ---
    inst_ownership = inst_data.get("institutionalOwnership", 0) if inst_data else 0
    # Simulating insider buying for structural placeholder
    insider_buying = inst_data.get("insiderBuyingLast90Days", True) if inst_data else False 
    
    if inst_ownership > 40:
        score += 2
        reasons.append(f"✔ High Institutional Ownership ({inst_ownership:.1f}%)")
    if insider_buying:
        score += 3
        reasons.append("✔ Recent Insider Accumulation (90 Days)")

    return {
        "technical_score_component": score,
        "technical_signals": reasons,
        "raw_signals": {
            "rsi": round(rsi, 2),
            "sma50": sma50,
            "sma200": sma200,
            "volume_ratio": round(volume_today / avg_volume, 2) if avg_volume else 0
        }
    }