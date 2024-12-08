import sys
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline
from src.constant import *
from src.exception import CustomException
from src.logger import logging
from src.utlis.main_utils import MainUtils
from dataclasses import dataclass

@dataclass
class DataTransFormationConfig:
    artifact_dir = os.path.join(artifact_folder)
    transformed_train_file_path = os.path.join(artifact_dir, 'train.npy')
    transformed_test_file_path = os.path.join(artifact_dir, 'test.npy')
    transformed_object_file_path = os.path.join(artifact_dir, 'preprocessor.pkl')


class DataTransformation:
    def __init__(self, feature_store_file_path):
        self.feature_store_file_path = feature_store_file_path
        self.data_transformation_config = DataTransFormationConfig()
        self.utils = MainUtils()

    @staticmethod
    def get_data(feature_store_file_path: str) -> pd.DataFrame:
        try:
            logging.info(f"Reading data from {feature_store_file_path}")
            data = pd.read_csv(feature_store_file_path)
            data.rename(columns={"Good/Bad": TARGET_COLUMN}, inplace=True)
            logging.info("Data loaded and column renamed successfully.")
            return data
        except Exception as e:
            logging.error(f"Error in loading data from {feature_store_file_path}: {str(e)}")
            raise CustomException(e, sys)

    def get_data_transformer_object(self):
        try:
            imputer_step = ('imputer', SimpleImputer(strategy='constant', fill_value=0))
            scaler_step = ('scaler', RobustScaler())
            preprocessor = Pipeline(
                steps=[
                    imputer_step,
                    scaler_step
                ]
            )
            return preprocessor
        except Exception as e:
            logging.error(f"Error in creating data transformer object: {str(e)}")
            raise CustomException(e, sys)

    def initiate_data_transformation(self):
        logging.info("Entered initiate_data_transformation method of DataTransformation class")

        try:
            dataframe = self.get_data(feature_store_file_path=self.feature_store_file_path)

            x = dataframe.drop(columns=TARGET_COLUMN)
            y = np.where(dataframe[TARGET_COLUMN] == -1, 0, 1)

            X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

            preprocessor = self.get_data_transformer_object()

            X_train_scaled = preprocessor.fit_transform(X_train)
            X_test_scaled = preprocessor.transform(X_test)

            preprocessor_path = self.data_transformation_config.transformed_object_file_path
            os.makedirs(os.path.dirname(preprocessor_path), exist_ok=True)

            self.utils.save_object(file_path=preprocessor_path, obj=preprocessor)

            train_arr = np.column_stack([X_train_scaled, np.array(y_train)])
            test_arr = np.column_stack([X_test_scaled, np.array(y_test)])

            logging.info("Data transformation completed successfully.")
            return train_arr, test_arr, preprocessor_path

        except Exception as e:
            logging.error("Error during data transformation")
            raise CustomException(e, sys)

            
            
        
             
        
        
        
        
        
            
        
        
        
    
    
        
        
        
     
    