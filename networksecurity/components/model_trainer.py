import os,sys 

from networksecurity.exception.CustomException import NetworkSecurityException
from networksecurity.logging.logger import logger_function 
from networksecurity.entity.artifacts_entity import DataTransformationArtifcat, ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig 


from networksecurity.utils.ml_utils.model_estimator import NetworkModel 
from networksecurity.utils.main_utils.code_utils import save_object, load_object, load_numpy_array_data, evaluate_models 
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score 


from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier 
import mlflow 
from urllib.parse import urlparse 
import dagshub
dagshub.init(repo_owner='muralik98', repo_name='networksecurityclassification', mlflow=True)

#os.environ["MLFLOW_TRACKING_URI"]=""
#os.environ["MLFLOW_TRACKING_USERNAME"]=""
#os.environ["MLFLOW_TRACKING_PASSWORD"]=""


class ModelTrainer:

    def __init__(self, model_trainer_config:ModelTrainerConfig, data_transformation_artifact:DataTransformationArtifcat):
        try:
            self.model_trainer_config=model_trainer_config 
            self.data_transformation_artifact=data_transformation_artifact 
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def track_mlflow(self, best_model, classification_metric):
        mlflow.set_registry_uri("")  # set local path or dagshub-path 
        with mlflow.start_run():
            f1_score=classification_metric.f1_score
            precesion_score=classification_metric.precision_score 
            recall_score=classification_metric.recall_score 

            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("precision",precesion_score)
            mlflow.log_metric("recall_score",recall_score)
            mlflow.sklearn.log_model(best_model,"model")

            if tracking_url_type_store != "file":

                # Register the model
                # There are other ways to use the Model Registry, which depends on the use case,
                # please refer to the doc for more information:
                # https://mlflow.org/docs/latest/model-registry.html#api-workflow
                mlflow.sklearn.log_model(best_model, "model", registered_model_name=best_model)
            else:
                mlflow.sklearn.log_model(best_model, "model")

    def train_model(self,X_train,y_train,x_test,y_test):
        models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
            }
        params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
            
        }
        model_report:dict=evaluate_models(X_train=X_train,y_train=y_train,X_test=x_test,y_test=y_test,
                                    models=models,param=params)
    
        ## To get best model score from dict
        best_model_score = max(sorted(model_report.values()))

        ## To get best model name from dict

        best_model_name = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)       # check 
        ]
        best_model = models[best_model_name]
        y_train_pred=best_model.predict(X_train)

        classification_train_metric=get_classification_score(y_true=y_train, y_pred=y_train_pred )
        self.track_mlflow(best_model, classmetric)

        y_test_pred=model.predict(x_test)

        classification_test_metric = get_classification_score(y_true=y_test y_pred=y_test_pred )

        self.track_mlflow(best_model, classification_test_metric)

        reprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok=True)

        Network_Model=NetworkModel(preprocessor=preprocessor,model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path,obj=NetworkModel)
        #model pusher
        save_object("final_model/model.pkl",best_model)
        

        ## Model Trainer Artifact
        model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                             train_metric_artifact=classification_train_metric,
                             test_metric_artifact=classification_test_metric
                             )
        logging.info(f"Model trainer artifact: {model_trainer_artifact}")
        return model_trainer_artifact
    

    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            #loading training array and testing array
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            model_trainer_artifact=self.train_model(x_train,y_train,x_test,y_test)
            return model_trainer_artifact

            
        except Exception as e:
            raise NetworkSecurityException(e,sys)


