from typing import List, Dict
from ibm_watsonx_orchestrate.agent_builder.tools import tool
import json 


@tool(
    name="BidCalculator",
    description="The core engine. Analyzes the RFP's specs against the provided product catalog and returns the best matching SKU, the calculated match score (%), and the total project price.",
)
def analyze_and_price_bid(
    rfp_specs_json: str,
    product_catalog_json: str,
    test_costs_json: str,
    required_tests_json: str
) -> Dict:
    """
    Performs Spec Match and Pricing Calculation in one unified step.

    Args:
        rfp_specs_json: JSON string with RFP requirements (e.g., {"voltage": 1100, "insulation": "XLPE", "quantity": 5000, "test_duration": 24}).
        product_catalog_json: JSON string of the entire product catalog data (List of Dicts).
        test_costs_json: JSON string of test costs data (List of Dicts).
        required_tests_json: JSON string listing tests required by the RFP (e.g., ["HV Test", "SC Test"]).

    Returns:
        A dictionary containing the top SKU, match score, and final calculated total price.
    """
    
    # --- 1. DATA PARSING & VALIDATION ---
    try:
        rfp_specs = json.loads(rfp_specs_json)
        product_catalog = json.loads(product_catalog_json)
        test_costs = json.loads(test_costs_json)
        required_tests = json.loads(required_tests_json)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON input received. Ensure all inputs are correctly formatted JSON strings."}
    
    # Check for empty catalog
    if not product_catalog:
        return {"error": "Product catalog is empty. Cannot perform analysis."}

    # Define Weights and required parameters
    WEIGHTS = {"voltage": 0.50, "insulation": 0.30, "min_length": 0.20}
    total_possible_weight = sum(WEIGHTS.values())
    
    # --- 2. SPEC MATCH CALCULATION ---
    best_match = None
    best_score = -1.0
    required_quantity = rfp_specs.get('quantity', 1)

    for product in product_catalog:
        current_score = 0.0
        
        # Data Type Cleaning (CRITICAL for safe comparison)
        try:
            prod_voltage = int(product.get('Voltage_Rating', 0))
            prod_insulation = product.get('Insulation_Type', '').upper()
            prod_length = int(product.get('Length_M', 0))
            prod_cost = float(product.get('Unit_Cost', 0.0))
        except (ValueError, TypeError):
            continue # Skip invalid rows
            
        # Score Calculation Logic (Same as before)
        if prod_voltage >= rfp_specs.get('voltage', 0):
            current_score += WEIGHTS['voltage']
        if prod_insulation == rfp_specs.get('insulation', '').upper():
            current_score += WEIGHTS['insulation']
        if prod_length >= rfp_specs.get('min_length', 0):
            current_score += WEIGHTS['min_length']
            
        match_percentage = (current_score / total_possible_weight) * 100
        
        if match_percentage > best_score:
            best_score = match_percentage
            best_match = product
            best_match['match_score'] = round(best_score, 2)
            best_match['material_cost'] = round(prod_cost * required_quantity, 2)
    
    if not best_match:
        return {"error": "No viable product found that meets minimum specification thresholds."}

    # --- 3. PRICING CALCULATION (Merger of Pricing Agent) ---
    total_test_cost = 0.0
    for required_test in required_tests:
        # Find test cost in the provided test_costs list
        cost_item = next((item for item in test_costs if item.get('Test_Name') == required_test), None)
        if cost_item:
            try:
                total_test_cost += float(cost_item.get('Base_Cost', 0))
            except ValueError:
                # Log error but continue with 0 cost for this test
                pass 
                
    final_price = best_match['material_cost'] + total_test_cost
    
    # --- 4. FINAL OUTPUT ---
    return {
        "final_status": "SUCCESS",
        "best_sku": best_match['SKU_ID'],
        "match_percentage": best_match['match_score'],
        "material_cost": best_match['material_cost'],
        "total_test_cost": total_test_cost,
        "final_bid_price": round(final_price, 2)
    }