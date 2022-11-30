import pandas as pd
import os
import datetime

import itertools

df = pd.read_csv("cleaned_data.csv")

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
        print(files)
        for file in files:
            task_id = int(file.split(".txt")[0][-1])
            patient_df = pd.read_csv(
                f"{patient_directory}/task_{task_id}.txt",
                header=None,
            )
            print(f" Processing task {task_id}")

            _, first_row_data = list(patient_df.iterrows())[0]

            start_time = datetime.datetime.strptime(
                first_row_data[TIMESTAMP_COL], "%H:%M:%S"
            )

            for _, data in patient_df.iterrows():
                time = data[TIMESTAMP_COL]
                try:
                    time = datetime.datetime.strptime(time, "%H:%M:%S.%f") - start_time
                    time = time.total_seconds()
                except:
                    time = (datetime.datetime.strptime(time, "%H:%M:%S")) - start_time
                    time = time.total_seconds()
                row_data = [
                    task_id,
                    time,
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
                    data[FOG_LABEL_COL],
                ]
                patient_data.append(row_data)
    print(f"Completed processing for patient {patient_id}!")
    return patient_data


all_patient_data = []
for i in range(3, 4):
    all_patient_data.extend(process_patient(i))

df = pd.DataFrame(
    all_patient_data,
    columns=[
        "subject_ID",
        "time",
        "imu_shank_l_ax",
        "imu_shank_l_ay",
        "imu_shank_l_az",
        "imu_shank_l_gx",
        "imu_shank_l_gy",
        "imu_shank_l_gz",
        "imu_shank_r_ax",
        "imu_shank_r_ay",
        "imu_shank_r_az",
        "imu_shank_r_gx",
        "imu_shank_r_gy",
        "imu_shank_r_gz",
        "imu_waist_ax",
        "imu_waist_ay",
        "imu_waist_az",
        "imu_waist_gx",
        "imu_waist_gy",
        "imu_waist_gz",
        "imu_arm_ax",
        "imu_arm_ay",
        "imu_arm_az",
        "imu_arm_gx",
        "imu_arm_gy",
        "imu_arm_gz",
        "freeze_label",
    ],
)
df.to_csv("cleaned_data_IMU_only.csv", index=False)
