from sensor.exception import SensorException
from sensor.logger import logging
import sys,os
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sensor.entity.config_entity import DataIngestionConfig
from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.data_access.sensor_data import SensorData


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise SensorException(e, sys)

    def export_data_into_feature_store(self)->DataIngestionArtifact:
        """
        Export data from mongodb
        """
        try:
            logging.info("Exporting data from mongodb to feature store")
            sensor_data = SensorData()
            dataframe = sensor_data.export_collection_as_dataframe(
                collection_name=self.data_ingestion_config.collection_name
            )
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            # creating folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)

            logging.info(f"Dataframe is written to {feature_store_file_path}")
            return dataframe
        except Exception as e:
            raise SensorException(e, sys)

    def split_data_as_train_test(self,dataframe:DataFrame)->None:
        try:
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=42)
            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Exporting train and test file path.")
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            logging.info(f"Exported train and test file path.")
            return train_set, test_set
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            dataframe=self.export_data_into_feature_store()
            dataframe = self.split_data_as_train_test(dataframe=dataframe)
            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                          test_file_path=self.data_ingestion_config.testing_file_path)
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e, sys)

