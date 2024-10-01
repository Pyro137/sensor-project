from sensor.entity.config_entity import ModelTrainerConfig
from sensor.entity.artifact_entity import ModelTrainerArtifact,DataTransformationArtifact
from sensor.exception import SensorException
from sensor.logger import logging
import sys,os
from sensor.utils.main_utils import load_numpy_array_data
from xgboost import XGBClassifier
from sensor.ml.metrics.clf_metrics import get_classification_scores
from sensor.ml.model.model_estimator import SensorModel
from sensor.utils.main_utils import load_object,save_object



class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,
        data_transformation_artifact:DataTransformationArtifact):
        try:    
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise SensorException(e, sys) from e
        
    def perform_hyper_parameter_tuning(self):
        pass

    def train_model(self,x_train,y_train):
        try:
            xgb_clf=XGBClassifier()
            xgb_clf.fit(x_train,y_train)
            return xgb_clf
        except Exception as e:
            raise SensorException(e, sys) from e
        
    def initiate_model_trainer(self):
        try:
            test_file_path=self.data_transformation_artifact.transformed_test_file_path
            train_file_path=self.data_transformation_artifact.transformed_train_file_path
            train_arr=load_numpy_array_data(train_file_path)
            test_arr=load_numpy_array_data(test_file_path)

            x_train,y_train,x_test,y_test=(
                train_arr[:, :-1],
                train_arr[:,-1],
                test_arr[:, :-1],
                test_arr[:,-1]
                )
            model=self.train_model(x_train,y_train)
            y_train_pred=model.predict(x_train)
            train_clf_metric=get_classification_scores(y_train,y_train_pred)

            
            y_test_pred=model.predict(x_test)
            test_clf_metric=get_classification_scores(y_test,y_test_pred)

            if train_clf_metric >=self.model_trainer_config.expected_accuracy:
                raise Exception('Train accuracy is not good')

            #overfittin and underfitting

            diff=abs(train_clf_metric.f1_score-test_clf_metric.f1_score)

            if diff<self.model_trainer_config.overfitting_underfitting_threshold:
                logging.info("No Overfitting or Underfitting")
            else:
                logging.info("Overfitting or Underfitting")
            
            preprocessor=load_object(self.data_transformation_artifact.transformed_object_file_path)

            model_dir_path=self.model_trainer_config.trained_model_file_path
            os.makedirs(model_dir_path,exist_ok=True)
            sensorModel=SensorModel(preprocessor,model=model)
            save_object(self.model_trainer_config.trained_model_file_path,obj=sensorModel)

            #artifact
            model_trainer_artifact=ModelTrainerArtifact(
                train_classification_scores=train_clf_metric,
                test_classification_scores=test_clf_metric,
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            )
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            raise SensorException(e, sys) from e

