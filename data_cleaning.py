import pandas as pd
import os

base_path = current_dir = os.path.dirname(__file__)

data_path = f"{base_path}/data"


# declare constant columns
TIMESTAMP_COL = 1
IO_COLUMN = 29
LEFT_SHANK_STARTING_COL = 32
RIGHT_SHANK_STARTING_COL = 39
WAIST_STARTING_COL = 46
ARM_STARTING_COL = 53
SC_COL = 59
FOG_LABEL_COL = 60


PATIENT_EMG_MAP = {  # for each patient, map columns in order of R_TA, L_TA, ECG, R_GS
    1: (27, 28, 30, 31),
    2: (27, 28, 30, 31),
    3: (28, 27, 30, 31),
    4: (28, 27, 30, 31),
    5: (28, 27, 30, 31),
    6: (27, 28, 30, 31),
    7: (27, 28, 30, 31),
    8: (27, 28, 30, 31),
    9: (28, 27, 30, 31),
    10: (28, 27, 30, 31),
    11: (28, 27, 30, 31),
    12: (28, 27, 30, 31),
    13: (27, 31, 30, 28),
}

PATIENT_FILE_SUBDIR_MAPPING = {
    1: "001",
    2: "002",
    3: "003",
    4: "004",
    5: "005",
    6: "006",
    7: "007",
    8: "008/OFF_1",
    9: "009",
    10: "010",
    11: "011",
    12: "012",
    13: "008/OFF_2",
}

# treat 8-1 as 8, 8-2 as 13
def process_patient(patient_id):
    print(f"Processing patient {patient_id}...")
    R_TA_COL, L_TA_COL, ECG_COL, R_GS_COL = PATIENT_EMG_MAP[patient_id]
    patient_directory = f"{data_path}/{PATIENT_FILE_SUBDIR_MAPPING[patient_id]}"
    patient_data = []
    for _, _, files in os.walk(patient_directory):
        for file in files:
            task_id = int(file.split(".txt")[0][-1])
            patient_df = pd.read_csv(
                f"{patient_directory}/task_{task_id}.txt",
                header=None,
            )
            print(f" Processing task {task_id}")

            for _, data in patient_df.iterrows():
                row_data = [
                    data[TIMESTAMP_COL],
                    patient_id,
                    task_id,
                    data[IO_COLUMN],
                    data[ECG_COL],
                    data[R_TA_COL],
                    data[L_TA_COL],
                    data[R_GS_COL],
                    data[LEFT_SHANK_STARTING_COL],
                    data[LEFT_SHANK_STARTING_COL + 1],
                    data[LEFT_SHANK_STARTING_COL + 2],
                    data[LEFT_SHANK_STARTING_COL + 3],
                    data[LEFT_SHANK_STARTING_COL + 4],
                    data[LEFT_SHANK_STARTING_COL + 5],
                    data[RIGHT_SHANK_STARTING_COL],
                    data[RIGHT_SHANK_STARTING_COL + 1],
                    data[RIGHT_SHANK_STARTING_COL + 2],
                    data[RIGHT_SHANK_STARTING_COL + 3],
                    data[RIGHT_SHANK_STARTING_COL + 4],
                    data[RIGHT_SHANK_STARTING_COL + 5],
                    data[WAIST_STARTING_COL],
                    data[WAIST_STARTING_COL + 1],
                    data[WAIST_STARTING_COL + 2],
                    data[WAIST_STARTING_COL + 3],
                    data[WAIST_STARTING_COL + 4],
                    data[WAIST_STARTING_COL + 5],
                    data[ARM_STARTING_COL],
                    data[ARM_STARTING_COL + 1],
                    data[ARM_STARTING_COL + 2],
                    data[ARM_STARTING_COL + 3],
                    data[ARM_STARTING_COL + 4],
                    data[ARM_STARTING_COL + 5],
                    data[SC_COL],
                    data[FOG_LABEL_COL],
                ]
                patient_data.append(row_data)
    print(f"Completed processing for patient {patient_id}!")
    return patient_data


all_patient_data = []
for i in range(1, 14):
    all_patient_data.extend(process_patient(i))

df = pd.DataFrame(
    all_patient_data,
    columns=[
        "Timestamp",
        "Patient_ID",
        "Task_ID",
        "Electrooculogram",
        "ECG",
        "EMG_R-TA",
        "EMG_L-TA",
        "EMG_R-GS",
        "LS_acc_x",
        "LS_acc_y",
        "LS_acc_z",
        "LS_gyro_x",
        "LS_gyro_y",
        "LS_gyro_z",
        "RS_acc_x",
        "RS_acc_y",
        "RS_acc_z",
        "RS_gyro_x",
        "RS_gyro_y",
        "RS_gyro_z",
        "Waist_acc_x",
        "Waist_acc_y",
        "Waist_acc_z",
        "Waist_gyro_x",
        "Waist_gyro_y",
        "Waist_gyro_z",
        "Arm_acc_x",
        "Arm_acc_y",
        "Arm_acc_z",
        "Arm_gyro_x",
        "Arm_gyro_y",
        "Arm_gyro_z",
        "SC",
        "FoG",
    ],
)
df.to_csv("cleaned_data.csv", index=False)
