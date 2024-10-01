from sensor.entity.artifact_entity import ClassificationMetricArtifact
from sklearn.metrics import f1_score,precision_score,recall_score
from sensor.exception import SensorException
import sys
def get_classification_scores(y_true,y_pred)->ClassificationMetricArtifact:

    try:
        f1=f1_score(y_true,y_pred)
        recall=recall_score(y_true,y_pred)
        precision=precision_score(y_true,y_pred)
        clf_metrics= ClassificationMetricArtifact(
            f1_score=f1,
            recall_score=recall,
            precision_score=precision,
        )
        return clf_metrics
    except Exception as e:
        raise SensorException(e,sys)
        