import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def test_api():
    print("Testing API...")
    
    # 1. GET /candidates
    print("\n1. GET /candidates")
    res = requests.get(f"{BASE_URL}/candidates")
    candidates = res.json()
    print(f"Status: {res.status_code}")
    print(f"Total candidates seeded: {len(candidates)}")
    assert len(candidates) >= 15, "Expected at least 15 seeded candidates"
    
    # 2. GET /candidates?stage=Screening
    print("\n2. GET /candidates?stage=Screening")
    res = requests.get(f"{BASE_URL}/candidates?stage=Screening")
    screening = res.json()
    print(f"Status: {res.status_code}")
    print(f"Candidates in Screening: {len(screening)}")
    assert all(c["stage"] == "Screening" for c in screening), "Filter didn't work"
    
    # 3. POST /candidates
    print("\n3. POST /candidates")
    new_candidate = {
        "name": "Test User",
        "stage": "Applying Period",
        "application_date": "2024-08-11",
        "overall_score": 5.0,
        "referred": True,
        "assessment_status": "Completed"
    }
    res = requests.post(f"{BASE_URL}/candidates", json=new_candidate)
    created = res.json()
    print(f"Status: {res.status_code}")
    print(f"Created ID: {created.get('id')}")
    assert created["name"] == "Test User", "Creation failed"
    c_id = created["id"]
    
    # Verify in GET
    res = requests.get(f"{BASE_URL}/candidates/{c_id}")
    assert res.status_code == 200, "Could not fetch created candidate"
    
    # 4. PUT /candidates/{id}
    print(f"\n4. PUT /candidates/{c_id}")
    update_data = {"overall_score": 4.5}
    res = requests.put(f"{BASE_URL}/candidates/{c_id}", json=update_data)
    updated = res.json()
    print(f"Status: {res.status_code}")
    print(f"Updated score: {updated.get('overall_score')}")
    assert updated["overall_score"] == 4.5, "Update failed"
    
    # 5. PATCH /candidates/{id}/stage
    print(f"\n5. PATCH /candidates/{c_id}/stage")
    res = requests.patch(f"{BASE_URL}/candidates/{c_id}/stage", json={"stage": "Test"})
    patched = res.json()
    print(f"Status: {res.status_code}")
    print(f"New stage: {patched.get('stage')}")
    assert patched["stage"] == "Test", "Patch failed"
    
    # 6. DELETE /candidates/{id}
    print(f"\n6. DELETE /candidates/{c_id}")
    res = requests.delete(f"{BASE_URL}/candidates/{c_id}")
    print(f"Status: {res.status_code}")
    
    # Verify deletion
    res = requests.get(f"{BASE_URL}/candidates/{c_id}")
    assert res.status_code == 404, "Deletion failed"
    
    # 7. GET /candidates with pagination and sorting
    print("\n7. GET /candidates?skip=0&limit=5&sort_by=overall_score&order=desc")
    res = requests.get(f"{BASE_URL}/candidates?skip=0&limit=5&sort_by=overall_score&order=desc")
    sorted_paged = res.json()
    print(f"Status: {res.status_code}")
    print(f"Count returned: {len(sorted_paged)}")
    for c in sorted_paged:
        print(f"  - {c['name']} (Score: {c['overall_score']})")
        
    print("\nAll endpoints verified successfully!")

if __name__ == "__main__":
    test_api()
