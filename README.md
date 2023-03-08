# Online Freezing of Gait Detection using LSTM-FCN

Abstract — Freezing of Gait (FoG) is a debilitating symptom of Parkinson’s Disease (PD) that causes an episodic reduction in the ability to walk forward despite an intention. The ability to predict future FoG from time-series sensor data in real-time has the potential to prevent patients from serious injury. Various machine learning and neural networks have been specifically applied to perform this task. A new dataset consisting of various multimodal sensors with FoG labels was collected from several trials performed by patients with PD. This data was then preprocessed and prepared for time series models. Various model architectures including RNNs, LSTMs, and an LSTM-FCN were then applied to this preprocessed data. By performing hyperparameter tuning with manual methods and Optuna, the LSTM-FCN model was able to achieve an F1 score of 90.4% and a specificity score of 96.1% for predicting FoG label 0.5-seconds in advance. The results from this model were compared to the other models and analyzed to extract insights into potential improvements for online FoG prediction. 

Final Project for SYDE 599 (Deep Learning)


Authors: Flynn Gurnsey, James Carr-Pries, Jennifer Chen, Jeffrey Ng, Cooper Ang
