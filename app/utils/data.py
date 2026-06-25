# app/utils/data.py

FACILITIES = {
    "1001": {
        "name": "Sunrise Care Center",
        "star_rating": 4,
        "hospitalizations": 12,
        "staffing_score": 3.8,
        "inspection_score": 88
    },
    "1002": {
        "name": "Green Valley Nursing Home",
        "star_rating": 3,
        "hospitalizations": 25,
        "staffing_score": 3.2,
        "inspection_score": 79
    },
    "1003": {
        "name": "Riverbend Skilled Nursing",
        "star_rating": 5,
        "hospitalizations": 8,
        "staffing_score": 4.5,
        "inspection_score": 94
    }
}

def get_facility(facility_id):
    return FACILITIES.get(facility_id)
