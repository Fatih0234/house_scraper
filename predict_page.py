
import streamlit as st
import pickle
import pandas as pd

def show_predict_page():
    # List of cities

    cities = ['Los Angeles', 'Santa Monica', 'Monrovia', 'Marina Del Rey', 'Studio City', 'Hollywood Hills', 'Long Beach', 'Van Nuys', 'Playa Vista', 'Sherman Oaks', 'West Hollywood', 'Pasadena', 'Reseda', 'Burbank', 'Pico Rivera', 'Canyon Country', 'Hollywood', 'Tarzana', 'Winnetka', 'Montebello', 'Glendale', 'North Hollywood', 'Lancaster', 'reseda', 'lancaster', 'San Dimas', 'Northridge', 'Encino', 'West Covina', 'Sunland', 'Woodland Hills', 'Arcadia', 'Hacienda Heights', 'Agoura Hills', 'Valley Village', 'West Hills', 'Marina del Rey', 'Culver City', 'Inglewood', 'Sherman Village', 'Alhambra', 'Carson', '90046', '90068', 'Santa Clarita', 'Stevenson Ranch', 'Covina', 'Mar Vista', 'Lomita', 'Hawthorne', 'Leimert Park', 'Lake Balboa', 'Harbor City', 'West Los Angeles', 'korea town', 'Torrance', 'Chatsworth', 'valley village', 'Valencia', 'Panorama City', 'Pomona', 'North Hills', 'VENICE', 'Canoga Park', 'and 13', 'Westwood', 'LOS ANGELES', 'Highland Park', 'Venice', 'Norwalk', 'Valley Glen 91401', 'NORTHRIDGE/GRANADA HILLS /PORTER RANCH', 'Los Angeles Ca', 'Downey', 'Toluca Lake', 'Redondo Beach', 'El Segundo', 'Gardena', 'Los ANgeles', 'Lakewood', 'Culver City Adjacent', 'Granada Hills', 'Glendora', 'Rowland Heights', 'Rampart Village', 'Palmdale', 'Van Nuys Ca. 91411', '45', 'PACOIMA', 'Panorama City Ca 91402', 'Bellflower', 'Monterey Park', 'La Verne', 'Rancho Palos Verdes CA', 'La Puente', 'La Crescenta', 'los Angeles', 'Los Angeles/Koreatown', 'La Puent', 'VENICE BEACH', 'Venice Beach', 'Los Feliz', 'WOODLAND HILLS', 'los angles', 'CA 91040', 'Palms', 'Mission Hills', 'Palisades', 'Westwood Village', 'Pico/Robertson', 'Lacrescenta', 'BRENTWOOD', 'Malibu', 'Whittier', 'Beverly Hills', 'Beverly Center', '90007', 'los angeles', '91401', 'San Gabriel', 'Rosemead', 'S. Redondo Beach', 'LA', 'El Monte', 'Cudahy', 'Blvd.', 'west hollywood', 'Bell', 'South Pasadena', 'Manhattan Beach', 'San Pedro', 'Santa monica', 'Rancho Palos Verdes', 'Signal Hill', 'Arleta', 'East Hollywood', 'LONG BEACH', 'san dimas', 'Cerritos', 'Sun Valley']

    # little info about the app
    st.title("House Rent Prediction App")
    st.write("""This app predicts the rent of a house based on various features that has been 
                scraped from Craigslist. At the moment, there is no url-paste-copy feature so 
                you need to input manually the features. The app uses XGBoost model to predict the rent.
                The model has been trained on a dataset of houses in Los Angeles, CA.""")
    # highlight this text
    st.markdown("**Note:** This app still in development and may have some bugs. Please report any bugs to the developer(sekanti02@gmail.com).")

    st.subheader("Prediction Inputs")

    # Input fields
    city = st.selectbox("City", cities)
    latitude = st.number_input("Latitude")
    longitude = st.number_input("Longitude")
    bed_rooms = st.number_input("Bedrooms")
    bath_rooms = st.number_input("Bathrooms")
    ft = st.number_input("Square Feet")
    # boolean values for features
    is_available_now = st.checkbox("Available Now")
    has_cats_ok = st.checkbox("Cats OK")
    has_dogs_ok = st.checkbox("Dogs OK")
    has_wd_in_unit = st.checkbox("Washer/Dryer In Unit")
    is_furnished = st.checkbox("Furnished")
    has_attached_garage = st.checkbox("Attached Garage")
    no_smoking = st.checkbox("No Smoking")
    is_wheelchair_accessible = st.checkbox("Wheelchair Accessible")
    has_air_conditioning = st.checkbox("Air Conditioning")
    has_ev_charging = st.checkbox("EV Charging")
    # Add more input fields as needed

    # Set default values for unchecked checkboxes
    default_false = False

    is_available_now = is_available_now if is_available_now is not None else default_false
    has_cats_ok = has_cats_ok if has_cats_ok is not None else default_false
    has_dogs_ok = has_dogs_ok if has_dogs_ok is not None else default_false
    has_wd_in_unit = has_wd_in_unit if has_wd_in_unit is not None else default_false
    is_furnished = is_furnished if is_furnished is not None else default_false
    has_attached_garage = has_attached_garage if has_attached_garage is not None else default_false
    no_smoking = no_smoking if no_smoking is not None else default_false
    is_wheelchair_accessible = is_wheelchair_accessible if is_wheelchair_accessible is not None else default_false
    has_air_conditioning = has_air_conditioning if has_air_conditioning is not None else default_false
    has_ev_charging = has_ev_charging if has_ev_charging is not None else default_false



    # Load your XGBoost model
    with open("xgboost_model.pkl", "rb") as f:
        model = pickle.load(f)

    # Create a DataFrame for prediction input
    prediction_input = pd.DataFrame({
        'city': [city],  # Assuming city is a string variable
        'latitude': [latitude],
        'longitude': [longitude],
        'bed_rooms': [bed_rooms],
        'bath_rooms': [bath_rooms],
        'ft': [ft],
        'is_available_now': [is_available_now],
        'has_cats_ok': [has_cats_ok],
        'has_dogs_ok': [has_dogs_ok],
        'has_wd_in_unit': [has_wd_in_unit],
        'is_furnished': [is_furnished],
        'has_attached_garage': [has_attached_garage],
        'no_smoking': [no_smoking],
        'is_wheelchair_accessible': [is_wheelchair_accessible],
        'has_air_conditioning': [has_air_conditioning],
        'has_ev_charging': [has_ev_charging]
    })

    if st.button("Predict"):
        prediction = model.predict(prediction_input)
        st.success(f"Predicted Rent: ${prediction[0]}")
