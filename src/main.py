import pickle
import pandas as pd
from src.models import User


# gender, age,
#                hypertension,
#                heart_disease, ever_married,
#                work_type, residence, glucose, bmi, smoking
def prediction_from_model(user: User):
    with open('../models/prediction_model.pkl', 'rb') as f:
        data = pickle.load(f)
    print(data)
    print(user.work_type)
    # work_type = user.work_type.lower().capitalize()
    # residence = user.residence.lower().capitalize()
    # smoking = user.smoking.lower().capitalize()

    if user.gender == 'MALE':
        gender = 1
    else:
        gender = 0

    if user.work_type.value == "Ребенок":
        work_type = 4
    elif user.work_type.value == "Государственная работа":
        work_type = 0
    elif user.work_type.value == "Не работал":
        work_type = 1
    elif user.work_type.value == "Конфиденциально":
        work_type = 2
    else:
        work_type = 3

    if user.residence_type.value == "Сельский":
        residence_type = 0
    else:
        residence_type = 1

    if user.smoking_status.value == "Раньше курил":
        smoking_status = 1
    elif user.smoking_status.value == "Никогда не курил":
        smoking_status = 2
    elif user.smoking_status.value == "Курю":
        smoking_status = 3
    else:
        smoking_status = 0

    with open('../models/min_max_scaler_avg_glucose_level.pkl', 'rb') as f:
        glucose = pickle.load(f)
        glucose_prd = glucose.transform([[user.avg_glucose_level]])[0][0]
        print(glucose_prd)
    with open('../models/min_max_scaler_bmi.pkl.', 'rb') as f:
        bmi = pickle.load(f)
        bmi_prd = bmi.transform([[user.bmi]])[0][0]
        print(bmi_prd)

    new_data = pd.DataFrame([[gender, user.age,
                              user.hypertension,
                              user.heart_disease, user.ever_married,
                            work_type, residence_type,glucose_prd, bmi_prd, smoking_status]],
                            columns=['gender', 'age', 'hypertension',
                                     'heart_disease', 'ever_married', 'work_type',
                                     'Residence_type', 'avg_glucose_level', 'bmi',
                                     'smoking_status'])
    prd = data.predict(new_data)

    return prd[0]
# print(prd[0])
